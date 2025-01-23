from typing import Union, Dict, Optional, Iterator

import pygame

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface, IUIElementInterface
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIContainerInterface

from pygame_gui.core import UIElement, UIContainer
from pygame_gui.core.drawable_shapes import RectDrawableShape, RoundedRectangleShape

from pygame_gui.core.gui_type_hints import Coordinate, RectLike
from .gui_type_dynamic_rect import DynamicRect

class UIDynamicContainer(UIElement, IContainerLikeInterface):
    """
    A rectangular panel that holds a UI container and is designed to overlap other elements. It
    acts a little like a window that is not shuffled about in a stack - instead remaining at the
    same layer distance from the container it was initially placed in.

    It's primary purpose is for things like involved HUDs in games that want to always sit on top
    of UI elements that may be present 'inside' the game world (e.g. player health bars). By
    creating a UI Panel at a height above the highest layer used by the game world's UI elements
    we can ensure that all elements added to the panel are always above the fray.

    :param relative_rect: The positioning and sizing rectangle for the panel. See the layout
                          guide for details.
    :param starting_height: How many layers above its container to place this panel on.
    :param manager: The GUI manager that handles drawing and updating the UI and interactions
                    between elements. If not provided or set to None,
                    it will try to use the first UIManager that was created by your application.
    :param margins: Controls the distance between the edge of the panel and where it's
                    container should begin.
    :param container: The container this panel is inside - distinct from this panel's own
                      container.
    :param parent_element: A hierarchical 'parent' used for signifying belonging and used in
                           theming and events.
    :param object_id: An identifier that can be used to help distinguish this particular panel
                      from others.
    :param anchors: Used to layout elements and dictate what the relative_rect is relative to.
                    Defaults to the top left.
    :param visible: Whether the element is visible by default. Warning - container visibility
                    may override this.
    """
    def __init__(self,
                 dynamic_rect: list[str],
                 starting_height: int = 1,
                 manager: Optional[IUIManagerInterface] = None,
                 *,
                 element_id: str = 'container',
                 margins: Optional[Dict[str, int]] = None,
                 paddings: Optional[Dict[str, int]] = None,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1
                 ):


        if margins is None:
            self.container_margins = {"left":   '0',
                                      "right":  '0',
                                      "top":    '0',
                                      "bottom": '0'}
        else:
            self.container_margins = margins

        self.container = container

        if self.container is None:
            size = manager.get_root_container().get_size()
            self.container_size = size
            self.window_size = size
        else:
            size = self.container.relative_rect.size
            self.container_size = size
            self.window_size = manager.get_root_container().get_size()
        self.screen_size = pygame.display.get_desktop_sizes()[0]

        self.dynamic_rect = DynamicRect(dynamic_rect, self, self.container_margins)


        self.relative_rect = self.dynamic_rect.get_rect()


        # Need to move some declarations early as they are indirectly referenced via the ui element
        # constructor
        self.panel_container = None
        super().__init__(self.relative_rect,
                         manager,
                         container,
                         starting_height=starting_height,
                         layer_thickness=1,
                         anchors=anchors,
                         visible=visible,
                         parent_element=parent_element,
                         object_id=object_id,
                         element_id=[element_id])

        self.background_colour = None
        self.border_colour = None
        self.background_image = None
        self.border_width = 0
        self.shadow_width = 0
        self.shape = 'rectangle'

        self.panel_container = UIContainer(self.relative_rect, manager,
                                           starting_height=starting_height,
                                           container=container,
                                           parent_element=self,
                                           object_id=ObjectID(object_id='#dynamic_container',
                                                              class_id=None),
                                           anchors=anchors,
                                           visible=self.visible)

        self.rebuild_from_changed_theme_data()


    def update(self, time_delta: float):
        """
        A method called every update cycle of our application. Designed to be overridden by derived
        classes but also has a little functionality to make sure the panel's layer 'thickness' is
        accurate and to handle window resizing.

        :param time_delta: time passed in seconds between one call to this method and the next.

        """
        super().update(time_delta)
        if self.get_container().get_thickness() != self.layer_thickness:
            self.layer_thickness = self.get_container().get_thickness()

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Can be overridden, also handle resizing windows. Gives UI Windows access to pygame events.
        Currently just blocks mouse click down events from passing through the panel.

        :param event: The event to process.

        :return: Should return True if this element consumes this event.

        """
        consumed_event = False
        if (self is not None and
                event.type == pygame.MOUSEBUTTONDOWN and
                event.button in [pygame.BUTTON_LEFT,
                                 pygame.BUTTON_RIGHT,
                                 pygame.BUTTON_MIDDLE]):
            scaled_mouse_pos = self.ui_manager.calculate_scaled_mouse_position(event.pos)
            if self.hover_point(scaled_mouse_pos[0], scaled_mouse_pos[1]):
                consumed_event = True

        return consumed_event

    def get_container(self) -> IUIContainerInterface:
        """
        Returns the container that should contain all the UI elements in this panel.

        :return UIContainer: The panel's container.

        """

        return self.panel_container

    def kill(self):
        """
        Overrides the basic kill() method of a pygame sprite so that we also kill all the UI
        elements in this panel.

        """
        self.get_container().kill()
        super().kill()

    def set_dimensions(self, dimensions: Coordinate, clamp_to_container: bool = False):
        """
        Set the size of this panel and then re-sizes and shifts the contents of the panel container
        to fit the new size.

        :param dimensions: The new dimensions to set.
        :param clamp_to_container: Whether we should clamp the dimensions to the
                                   dimensions of the container or not.

        """

        # Don't use a basic gate on this set dimensions method because the container may be a
        # different size to the window
        super().set_dimensions(dimensions)

        rect = self.dynamic_rect.get_rect()

        new_container_dimensions = (self.relative_rect.width - (self.container_margins['left'] +
                                                                self.container_margins['right']),
                                    self.relative_rect.height - (self.container_margins['top'] +
                                                                 self.container_margins['bottom']))
        if new_container_dimensions != self.get_container().get_size():
            self.get_container().set_dimensions(new_container_dimensions)

    def set_relative_position(self, position: Coordinate):
        """
        Method to directly set the relative rect position of an element.

        :param position: The new position to set.

        """
        super().set_relative_position(position)
        self.get_container().set_relative_position(self.relative_rect.topleft)

    def set_position(self, position: Coordinate):
        """
        Method to directly set the absolute screen rect position of an element.

        :param position: The new position to set.

        """
        super().set_position(position)
        self.get_container().set_relative_position(self.relative_rect.topleft)

    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a full rebuild of the
        button's drawable shape.
        """
        super().rebuild_from_changed_theme_data()
        has_any_changed = False

        background_colour = self.ui_theme.get_colour_or_gradient('dark_bg',
                                                                 self.combined_element_ids)
        if background_colour != self.background_colour:
            self.background_colour = background_colour
            has_any_changed = True

        border_colour = self.ui_theme.get_colour_or_gradient('normal_border',
                                                             self.combined_element_ids)
        if border_colour != self.border_colour:
            self.border_colour = border_colour
            has_any_changed = True

        background_image = None
        try:
            background_image = self.ui_theme.get_image('background_image',
                                                       self.combined_element_ids)
        except LookupError:
            background_image = None
        finally:
            if background_image != self.background_image:
                self.background_image = background_image
                has_any_changed = True

        # misc
        if self._check_misc_theme_data_changed(attribute_name='shape',
                                               default_value='rectangle',
                                               casting_func=str,
                                               allowed_values=['rectangle',
                                                               'rounded_rectangle']):
            has_any_changed = True

        if self._check_misc_theme_data_changed(attribute_name='tool_tip_delay',
                                               default_value=1.0,
                                               casting_func=float):
            has_any_changed = True

        if self._check_shape_theming_changed(defaults={'border_width': 1,
                                                       'shadow_width': 2,
                                                       'border_overlap': 1,
                                                       'shape_corner_radius': [2, 2, 2, 2]}):
            has_any_changed = True

        if has_any_changed:
            self.rebuild()

    def rebuild(self):
        pass
        """
        A complete rebuild of the drawable shape used by this button.

        """

        if self.container is None:
            size = self.ui_manager.get_root_container().get_size()
            self.container_size = size
            self.window_size = size
        else:
            size = self.container.relative_rect.size
            self.container_size = size
            self.window_size = self.ui_manager.get_root_container().get_size()
        self.screen_size = pygame.display.get_desktop_sizes()[0]

        self.relative_rect = self.dynamic_rect.get_rect()
        theming_parameters = {'normal_bg': self.background_colour,
                              'normal_border': self.border_colour,
                              'normal_image': self.background_image,
                              'border_width': 1,
                              'shadow_width': 0,
                              'shape_corner_radius': 0,
                              'border_overlap': 0}

        if self.shape == 'rectangle':
            self.drawable_shape = RectDrawableShape(self.relative_rect, theming_parameters,
                                                    ['normal'], self.ui_manager)
        elif self.shape == 'rounded_rectangle':
            self.drawable_shape = RoundedRectangleShape(self.relative_rect, theming_parameters,
                                                        ['normal'], self.ui_manager)

        self.on_fresh_drawable_shape_ready()

    def disable(self):
        """
        Disables all elements in the panel, so they are no longer interactive.
        """
        if self.is_enabled:
            self.is_enabled = False
            if self.panel_container is not None:
                self.panel_container.disable()

    def enable(self):
        """
        Enables all elements in the panel, so they are interactive again.
        """
        if not self.is_enabled:
            self.is_enabled = True
            if self.panel_container is not None:
                self.panel_container.enable()

    def show(self, show_contents: bool = True):
        """
        In addition to the base UIElement.show() - call show() of owned container - panel_container.

        :param show_contents: whether to also show the contents of the panel. Defaults to True.
        """
        super().show()
        if self.panel_container is not None:
            self.panel_container.show(show_contents)

    def hide(self, hide_contents: bool = True):
        """
        In addition to the base UIElement.hide() - call hide() of owned container - panel_container.

        :param hide_contents: whether to also hide the contents of the panel. Defaults to True.
        """
        if not self.visible:
            return

        if self.panel_container is not None:
            self.panel_container.hide(hide_contents)
        super().hide()

    def __iter__(self) -> Iterator[IUIElementInterface]:
        """
        Iterates over the elements within the container.
        :return Iterator: An iterator over the elements within the container.
        """
        return iter(self.get_container())

    def __contains__(self, item: IUIElementInterface) -> bool:
        """
        Checks if the given element is contained within the container.
        :param item: The element to check for containment.
        :return bool: Return True if the element is found, False otherwise.
        """
        return item in self.get_container()

    def are_contents_hovered(self) -> bool:
        """
        Are any of the elements in the container hovered? Used for handling mousewheel events.

        :return: True if one of the elements is hovered, False otherwise.
        """
        any_hovered = False
        for element in self:
            if any(sub_element.hovered for sub_element in element.get_focus_set()):
                any_hovered = True
            elif isinstance(element, IContainerLikeInterface):
                any_hovered = element.are_contents_hovered()

            if any_hovered:
                break
        return any_hovered

    def set_anchors(self, anchors: Optional[Dict[str, Union[str, IUIElementInterface]]]) -> None:
        super().set_anchors(anchors)
        if self.panel_container is not None:
            self.panel_container.set_anchors(anchors)
