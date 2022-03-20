from typing import Union

from discord import TextChannel, Role, Member, User, VoiceChannel
from discord.ext.commands import CommandError, Context

from core.global_enum import CollectionEnum, SubjectsOrGroupsEnum


################
# MONGO ERRORS #
################


class CouldNotEditEntryError(Exception):
    def __init__(self, collection: CollectionEnum, key: str, value: str = "<value>"):
        self.collection = collection
        self.key = key
        self.value = value


class BrokenConfigurationError(Exception):
    def __init__(self, collection: str, keys: Union[str, list[str]]):
        self.collection: str = collection
        if keys is str:
            self.keys: list[str] = [keys]
        else:
            self.keys: list[str] = keys

    def key_representation(self) -> str:
        output: str = str(self.keys).replace("'", "`")
        if "`" not in output:
            output = "`" + output + "`"
        return output


################
# ROLES ERRORS #
################


class FailedToGrantRoleError(CommandError):
    def __init__(self, role: Role, member: Union[Member, User]):
        self.role = role
        self.member = member


class YouAlreadyHaveThisSubjectError(CommandError):
    pass


class GroupOrSubjectNotFoundError(CommandError):
    def __init__(self, group: str, _type: SubjectsOrGroupsEnum):
        self.group = group
        self.type = _type


class CantAssignToSubject(CommandError):
    pass


class CantRemoveSubject(CommandError):
    pass


class YouNeedAStudyGroupError(CommandError):
    pass


###############
# TMPC ERRORS #
###############

class IsAlreadyAJoinChannelError(CommandError):
    def __init__(self, channel: VoiceChannel):
        assert isinstance(channel, VoiceChannel)
        self.channel = channel


class CouldNotFindToken(CommandError):
    pass


class WrongChatForCommandTmpc(CommandError):
    pass


class NameDuplicationError(CommandError):
    def __init__(self, name: str):
        self.name = name


class NotOwnerError(CommandError):
    def __init__(self, is_mod: bool, owner: str):
        self.is_mod = is_mod
        self.owner = owner


class LeaveOwnChannelError(CommandError):
    pass


class TempChannelMayNotPersistError(CommandError):
    pass


class YouOwnNoChannelsError(CommandError):
    pass


####################
# PREDICATE ERRORS #
####################


class NoMultipleGroupsError(CommandError):
    def __init__(self, role: Role):
        self.role = role


class NoBotChatError(CommandError):
    def __init__(self, channels: set[TextChannel]):
        self.channels = channels


class NoRulesError(CommandError):
    pass


##########
# OTHERS #
##########

class MentionNotFoundError(CommandError):
    def __init__(self, want, mention):
        self.want = want
        self.mention = mention


class ManPageNotFound(Exception):
    pass


class LinkingNotFoundError(CommandError):
    def __init__(self, ctx: Context):
        self.prefix = ctx.bot.command_prefix


class HasNoHandlerException(Exception):
    pass


class MissingInteractionError(CommandError):
    pass


class HitDiscordLimitsError(CommandError):
    def __init__(self, cause: str, solution: str):
        self.cause = cause
        self.solution = solution
