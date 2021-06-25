"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union
from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
try:
    from traits.trait_type import TraitType
except ModuleNotFoundError:
    from traits.traits import TraitType


class CommonOccultUtils:
    """Utilities for manipulating the Occults of Sims.

    """

    @staticmethod
    def get_sim_info_for_all_occults_gen(sim_info: SimInfo, exclude_occult_types: Iterator[OccultType]) -> Iterator[SimInfo]:
        """get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult Sim info will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: Iterator[OccultType]
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            return tuple()
        exclude_occult_types: Tuple[OccultType] = tuple(exclude_occult_types)
        yield sim_info
        for occult in OccultType.values:
            if occult in exclude_occult_types:
                continue
            # noinspection PyPropertyAccess
            if occult == sim_info.current_occult_types:
                continue
            if not sim_info.occult_tracker.has_occult_type(occult):
                continue
            occult_sim_info: SimInfo = sim_info.occult_tracker.get_occult_sim_info(occult)
            if occult_sim_info is None:
                continue
            yield occult_sim_info

    @staticmethod
    def has_any_occult(sim_info: SimInfo) -> bool:
        """has_any_occult(sim_info)

        Determine if a Sim has any Occult Types.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: True, if the specified Sim has any Non-Human Occult Types. False, if not.
        :rtype: bool
        """
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return False
        return sim_info.occult_tracker.has_any_occult_or_part_occult_trait()

    @staticmethod
    def has_occult_sim_info(sim_info: SimInfo, occult_type: OccultType) -> bool:
        """has_occult_sim_info(sim_info, occult_type)

        Determine if a Sim has a SimInfo for an Occult.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: True, if a SimInfo is available for the specified Occult for the Sim. False, if not.
        :rtype: bool
        """
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return False
        return sim_info.occult_tracker.has_occult_type(occult_type)

    @staticmethod
    def get_current_occult_sim_info(sim_info: SimInfo) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_current_occult_sim_info(sim_info)

        Retrieve the SimInfo for the Occult the Sim is currently.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the Occult they are (If they are currently an occult).
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        current_occult_type = CommonOccultUtils.get_current_occult_type(sim_info)
        return CommonOccultUtils.get_occult_sim_info(sim_info, current_occult_type)

    @staticmethod
    def get_occult_sim_info(sim_info: SimInfo, occult_type: OccultType) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_occult_sim_info(sim_info, occult_type)

        Retrieve the SimInfo for an Occult of a Sim.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to retrieve the SimInfo of.
        :type occult_type: OccultType
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the specified Occult.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if not CommonOccultUtils.has_occult_sim_info(sim_info, occult_type):
            return None
        return sim_info.occult_tracker.get_occult_sim_info(occult_type)

    @staticmethod
    def add_alien_occult(sim_info: SimInfo) -> bool:
        """add_alien_occult(sim_info)

        Add the Alien Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become an Alien. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_alien(sim_info):
            return True
        loot_action_ids: Tuple[int] = (
            # loot_Occult_AlienAdd
            103256,
            # loot_Occult_AlienSwitch
            103254
        )
        # noinspection PyPropertyAccess
        physique = sim_info.physique
        # noinspection PyPropertyAccess
        facial_attributes = sim_info.facial_attributes
        # noinspection PyPropertyAccess
        voice_pitch = sim_info.voice_pitch
        # noinspection PyPropertyAccess
        voice_actor = sim_info.voice_actor
        # noinspection PyPropertyAccess
        voice_effect = sim_info.voice_effect
        # noinspection PyPropertyAccess
        skin_tone = sim_info.skin_tone
        flags = sim_info.flags
        pelt_layers = None
        if hasattr(sim_info, 'pelt_layers'):
            # noinspection PyPropertyAccess
            pelt_layers = sim_info.pelt_layers
        base_trait_ids = None
        if hasattr(sim_info, 'base_trait_ids'):
            base_trait_ids = list(sim_info.base_trait_ids)
        # noinspection PyPropertyAccess
        genetic_data_b = sim_info.genetic_data
        if hasattr(genetic_data_b, 'SerializeToString'):
            genetic_data_b = genetic_data_b.SerializeToString()
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        human_sim_info = sim_info.occult_tracker.get_occult_sim_info(OccultType.HUMAN)
        human_sim_info.physique = physique
        human_sim_info.facial_attributes = facial_attributes
        human_sim_info.voice_pitch = voice_pitch
        human_sim_info.voice_actor = voice_actor
        human_sim_info.voice_effect = voice_effect
        human_sim_info.skin_tone = skin_tone
        human_sim_info.flags = flags
        if pelt_layers is not None:
            human_sim_info.pelt_layers = pelt_layers
        if base_trait_ids is not None:
            human_sim_info.base_trait_ids = list(base_trait_ids)
        if hasattr(human_sim_info.genetic_data, 'MergeFromString'):
            human_sim_info.genetic_data.MergeFromString(genetic_data_b)
        else:
            human_sim_info.genetic_data = genetic_data_b
        return result

    @staticmethod
    def remove_alien_occult(sim_info: SimInfo) -> bool:
        """remove_alien_occult(sim_info)

        Remove the Alien Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Alien Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_alien(sim_info):
            return True
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        sim_info.occult_tracker.remove_occult_type(OccultType.ALIEN)
        return True

    @staticmethod
    def add_mermaid_occult(sim_info: SimInfo) -> bool:
        """add_mermaid_occult(sim_info)

        Add the Mermaid Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Mermaid. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_mermaid(sim_info):
            return True
        # loot_Mermaid_DebugAdd
        add_loot_action_id = 205399
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_action_id, sim_info)
        return result

    @staticmethod
    def remove_mermaid_occult(sim_info: SimInfo) -> bool:
        """remove_mermaid_occult(sim_info)

        Remove the Mermaid Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Mermaid Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_mermaid(sim_info):
            return True
        trait_ids: Tuple[int] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TEMPORARY_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        return CommonTraitUtils.remove_trait(sim_info, *trait_ids)

    @staticmethod
    def add_servo_occult(sim_info: SimInfo) -> bool:
        """add_servo_occult(sim_info)

        Add the Servo Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Servo. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_robot(sim_info):
            return True

        return CommonTraitUtils.add_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @staticmethod
    def remove_servo_occult(sim_info: SimInfo) -> bool:
        """remove_servo_occult(sim_info)

        Remove the Servo Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Servo Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_robot(sim_info):
            return True
        return CommonTraitUtils.remove_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @staticmethod
    def add_skeleton_occult(sim_info: SimInfo) -> bool:
        """add_skeleton_occult(sim_info)

        Add the Skeleton Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Skeleton. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_skeleton(sim_info):
            return True
        # loot_Skeleton_Add
        add_loot_id = 175969
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_skeleton_occult(sim_info: SimInfo) -> bool:
        """remove_skeleton_occult(sim_info)

        Remove the Skeleton Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Skeleton Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_skeleton(sim_info):
            return True
        # loot_Skeleton_Remove
        remove_loot_id = 175975
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(remove_loot_id, sim_info)

    @staticmethod
    def add_vampire_occult(sim_info: SimInfo) -> bool:
        """add_vampire_occult(sim_info)

        Add the Vampire Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Vampire. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_vampire(sim_info):
            return True
        # loot_VampireCreation_NewVampire
        add_loot_id = 149538
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_vampire_occult(sim_info: SimInfo) -> bool:
        """remove_vampire_occult(sim_info)

        Remove the Vampire Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Vampire Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            return True
        loot_action_ids: Tuple[int] = (
            # loot_VampireCure_RemoveVampirism
            150170,
            # loot_Life_ResetProgress
            31238
        )
        return CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)

    @staticmethod
    def add_witch_occult(sim_info: SimInfo) -> bool:
        """add_witch_occult(sim_info)

        Add the Witch Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Witch. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_witch(sim_info):
            return True
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_witch_occult(sim_info: SimInfo) -> bool:
        """remove_witch_occult(sim_info)

        Remove the Witch Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Witch Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_witch(sim_info):
            return True
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_duo_sims(remove_loot_id, sim_info, sim_info)

    @staticmethod
    def add_all_occults(sim_info: SimInfo) -> bool:
        """add_all_occults(sim_info)

        Add all Occult Types to a Sim. i.e. Make them a Alien, Vampire, Witch, etc.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if all Occult Types were successfully added to the specified Sim. False, if not.
        :rtype: bool
        """
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        CommonOccultUtils.add_alien_occult(sim_info)
        CommonOccultUtils.add_mermaid_occult(sim_info)
        CommonOccultUtils.add_servo_occult(sim_info)
        CommonOccultUtils.add_skeleton_occult(sim_info)
        CommonOccultUtils.add_vampire_occult(sim_info)
        CommonOccultUtils.add_witch_occult(sim_info)
        return True

    @staticmethod
    def remove_all_occults(sim_info: SimInfo) -> bool:
        """remove_all_occults(sim_info)

        Remove all Occult Types from a Sim. i.e. Make them a Non-Occult only.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if all Occult Types were successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        CommonOccultUtils.remove_alien_occult(sim_info)
        CommonOccultUtils.remove_mermaid_occult(sim_info)
        CommonOccultUtils.remove_servo_occult(sim_info)
        CommonOccultUtils.remove_skeleton_occult(sim_info)
        CommonOccultUtils.remove_vampire_occult(sim_info)
        CommonOccultUtils.remove_witch_occult(sim_info)
        return True

    @staticmethod
    def switch_to_occult_form(sim_info: SimInfo, occult_type: OccultType) -> bool:
        """switch_to_occult_form(sim_info, occult_type)

        Switch a Sim to an Occult Form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The type of Occult to switch to.
        :type occult_type: OccultType
        :return: True, if the Sim successfully switched to the specified Occult Type. False, if the Sim failed to switch to the specified Occult Type or if they do not have that Occult Type to switch to.
        :rtype: bool
        """
        if not CommonOccultUtils.has_occult_sim_info(sim_info, occult_type):
            return False
        sim_info.occult_tracker.switch_to_occult_type(occult_type)
        return True

    @staticmethod
    def is_vampire(sim_info: SimInfo) -> bool:
        """is_vampire(sim_info)

        Determine if a Sim is a Vampire.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Vampire. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE)

    @staticmethod
    def is_alien(sim_info: SimInfo) -> bool:
        """is_alien(sim_info)

        Determine if a Sim is an Alien.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Alien. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN)

    @staticmethod
    def is_plant_sim(sim_info: SimInfo) -> bool:
        """is_plant_sim(sim_info)

        Determine if a Sim is a Plant Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Plant Sim. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM)

    @staticmethod
    def is_ghost(sim_info: SimInfo) -> bool:
        """is_ghost(sim_info)

        Determine if a Sim is a Ghost.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Ghost. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            is_ghost_trait = getattr(trait, 'is_ghost_trait', None)
            if is_ghost_trait:
                return True
        return False

    @staticmethod
    def is_robot(sim_info: SimInfo) -> bool:
        """is_robot(sim_info)

        Determine if a Sim is a Robot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Robot. False, if not.
        :rtype: bool
        """
        if not hasattr(TraitType, 'ROBOT'):
            return False
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            trait_type = getattr(trait, 'trait_type', -1)
            if trait_type == TraitType.ROBOT:
                return True
        return False
    
    @staticmethod
    def is_skeleton(sim_info: SimInfo) -> bool:
        """is_skeleton(sim_info)

        Determine if a Sim is a Skeleton.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is the a Skeleton. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        skeleton_trait_ids = {
            CommonTraitId.HIDDEN_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_SERVICE_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_TEMPLE_SKELETON
        }
        for trait in equipped_sim_traits:
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id in skeleton_trait_ids:
                return True
        return False

    @staticmethod
    def is_witch(sim_info: SimInfo) -> bool:
        """is_witch(sim_info)

        Determine if a Sim is a Witch

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Witch. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WITCH)

    @staticmethod
    def is_mermaid(sim_info: SimInfo) -> bool:
        """is_mermaid(sim_info)

        Determine if a Sim is a Mermaid

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID)

    @staticmethod
    def is_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_in_mermaid_form(sim_info)

        Determine if a Sim is in Mermaid Form (The Sim has a visible Tail).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has their Mermaid tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID_MERMAID_FORM)

    @staticmethod
    def is_mermaid_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_mermaid_in_mermaid_form(sim_info)

        Determine if a Sim is a Mermaid and is in Mermaid Form (Their Tail is visible).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid with their tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_mermaid(sim_info) and CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def is_currently_human(sim_info: SimInfo) -> bool:
        """is_currently_human(sim_info)

        Determine if a Sim is currently in their Human form (regardless of their Occult type).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently a Human. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'HUMAN'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.HUMAN

    @staticmethod
    def is_currently_a_mermaid(sim_info: SimInfo) -> bool:
        """is_currently_a_mermaid(sim_info)

        Determine if a Sim is currently in their Mermaid form. (Not disguised)

        .. note:: This only checks their current occult status, it does not check for a visible Tail.\
            Use :func:`~is_in_mermaid_form` to check for a visible Tail.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Mermaid form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'MERMAID'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.MERMAID

    @staticmethod
    def is_currently_a_vampire(sim_info: SimInfo) -> bool:
        """is_currently_a_vampire(sim_info)

        Determine if a Sim is currently in their Vampire form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Vampire form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'VAMPIRE'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.VAMPIRE

    @staticmethod
    def is_currently_an_alien(sim_info: SimInfo) -> bool:
        """is_currently_an_alien(sim_info)

        Determine if a Sim is currently in their Alien form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Alien form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'ALIEN'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.ALIEN

    @staticmethod
    def is_currently_a_witch(sim_info: SimInfo) -> bool:
        """is_currently_a_witch(sim_info)

        Determine if a Sim is currently in their Witch form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Witch form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'WITCH'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.WITCH

    @staticmethod
    def get_sim_info_of_all_occults_gen(sim_info: SimInfo, *exclude_occult_types: OccultType) -> Iterator[SimInfo]:
        """get_sim_info_of_all_occults_gen(sim_info, *exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. warning:: Obsolete, please use :func:`~get_sim_info_for_all_occults_gen` instead.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: OccultType
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        return CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

    @staticmethod
    def _has_occult_trait(sim_info: SimInfo, trait_id: Union[int, CommonTraitId]) -> bool:
        return CommonOccultUtils._has_occult_traits(sim_info, (trait_id,))

    @staticmethod
    def _has_occult_traits(sim_info: SimInfo, trait_ids: Iterator[Union[int, CommonTraitId]]) -> bool:
        if sim_info is None:
            return False
        equipped_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for equipped_trait in equipped_traits:
            trait_id = CommonTraitUtils.get_trait_id(equipped_trait)
            if trait_id in trait_ids:
                return True
        return False

    @staticmethod
    def get_current_occult_type(sim_info: SimInfo) -> OccultType:
        """get_current_occult_type(sim_info)

        Retrieve the current occult type of the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The current occult type of the Sim.
        :rtype: OccultType
        """
        if sim_info is None:
            return OccultType.HUMAN
        # noinspection PyPropertyAccess
        return sim_info.current_occult_types
