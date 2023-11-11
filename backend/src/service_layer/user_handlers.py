from __future__ import annotations
from dataclasses import asdict
from typing import List
from src.domain.users import commands, user_models
from src.adapters.repositories import user_repository


class UserAlreadyExist(Exception):
    pass


def create_account(cmd: commands.Command, repo: user_repository.AbstractUserRepository):
    account = repo.get(cmd.username)
    if account is None:
        account = user_models.Account() 
        user = user_models.User.create_user(cmd.username, cmd.email, cmd.password, cmd.first_name, cmd.last_name)
        account.set_user(user)
        repo.add(account)
        repo.session.commit()

    else:
        raise UserAlreadyExist()        