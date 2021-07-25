# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a scaffold of a model."""

from aea.skills.base import Model
from aea.helpers.transaction.base import Terms

class Strategy(Model):
    """This class scaffolds a model."""

    ledger_id = "ethereum"

    
    def __init__(self, *args, **kwargs):
        self.reward_contract_address = kwargs.pop("reward_contract_address")
        self.min_sushi = kwargs.pop("min_sushi")
        self.pending_sushi = 0
        self.transacting = False
        self.failed_txs = 0
        self.balance = 0
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        self.log = self.context.logger.info

        self.log(f"Agent Address {self.context.agent_address}")
        return super().setup()
    
    def get_deploy_terms(self) -> Terms:
        """
        Get deploy terms of deployment.
        :return: terms
        """
        terms = Terms(
            ledger_id=self.ledger_id,
            sender_address=self.context.agent_address,
            counterparty_address=self.context.agent_address,
            amount_by_currency_id={},
            quantities_by_good_id={},
            nonce="",
        )
        return terms
