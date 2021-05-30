"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from event_testing.results import TestResult
from interactions.context import InteractionContext
from objects.game_object import GameObject
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils


class S4CLDebugObjectFixInteraction(CommonImmediateSuperInteraction):
    """S4CLDebugObjectFixInteraction(*_, **__)

    Set the target Object to a fixed state.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_fix_object'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None or CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is None.')
            return TestResult.NONE
        interaction_target: GameObject = interaction_target
        if not CommonObjectStateUtils.is_broken(interaction_target):
            cls.get_log().debug('Failed, the Object is not broken.')
            return TestResult.NONE
        cls.get_log().debug('Success, can fix object.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: GameObject) -> bool:
        return CommonObjectStateUtils.fix_object(interaction_target)
