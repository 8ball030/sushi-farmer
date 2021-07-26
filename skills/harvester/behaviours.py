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

"""This package contains a scaffold of a behaviour."""

from aea.skills.behaviours import TickerBehaviour
from packages.fetchai.protocols.ledger_api.message import LedgerApiMessage
from packages.fetchai.protocols.contract_api.message import ContractApiMessage

from packages.eightballer.skills.harvester.strategy import Strategy
from packages.eightballer.skills.harvester.dialogues import LedgerApiDialogues, ContractApiDialogues
from typing import cast


from packages.fetchai.connections.ledger.base import (
    CONNECTION_ID as LEDGER_CONNECTION_PUBLIC_ID,
)

from aea.helpers.transaction.base import Terms
LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


class SushiFarmer(TickerBehaviour):

    """This class scaffolds a behaviour."""

    def __init__(self, **kwargs):
        self.service_interval = kwargs.pop('service_interval')
        super(SushiFarmer, self).__init__(
            tick_interval=self.service_interval, **kwargs)

    def _check_pids(self):
        self.log(f"Querying contract for available pools.")
        strategy = cast(Strategy, self.context.strategy)
        contract_api_dialogues = cast(
            ContractApiDialogues, self.context.contract_api_dialogues
        )
        contract_api_msg, contract_api_dialogue = contract_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=ContractApiMessage.Performative.GET_STATE,
            ledger_id=strategy.ledger_id,
            contract_id="eightballer/sushi_farm:0.1.0",
            contract_address=strategy.reward_contract_address,
            callable="poolLength",
            kwargs=ContractApiMessage.Kwargs(
                {}
            ),

        )
        self.context.outbox.put_message(message=contract_api_msg)
        

    def setup(self) -> None:
        """Implement the setup."""
        self.log = self.context.logger.info
        self.log(f"SushiFarmer started")
        self._check_pids()

    def _check_balance(self):
        strategy = cast(Strategy, self.context.strategy)
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, _ = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_BALANCE,
            ledger_id=strategy.ledger_id,
            address=cast(str, self.context.agent_addresses.get(
                strategy.ledger_id)),
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def _check_sushi(self, pid):
        strategy = cast(Strategy, self.context.strategy)
        contract_api_dialogues = cast(
            ContractApiDialogues, self.context.contract_api_dialogues
        )
        contract_api_msg, contract_api_dialogue = contract_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=ContractApiMessage.Performative.GET_STATE,
            ledger_id=strategy.ledger_id,
            contract_id="eightballer/sushi_farm:0.1.0",
            contract_address=strategy.reward_contract_address,
            callable="pendingSushi",
            kwargs=ContractApiMessage.Kwargs(
                {"pid": pid, "address": self.context.agent_address}
            ),

        )
        self.context.outbox.put_message(message=contract_api_msg)

    def act(self) -> None:
        """Implement the act."""
        strategy = cast(Strategy, self.context.strategy)
        
        self._check_balance()

        for pid in range(strategy.total_pids):
            self._check_sushi(pid)

        if strategy.transacting is True: return
        if strategy.failed_txs > 3:
            self.log("Failed to transact... Sorry boss.")
            return
        
        for pid, amt  in strategy.pending_sushi_pools.items():
            if amt > strategy.min_sushi:
                self.log(f"Harvesting sushi! {pid} {amt}")
                self._harvest_sushi(pid)
            

    def _harvest_sushi(self, pid) -> None:
        strategy = cast(Strategy, self.context.strategy)
        contract_api_dialogues = cast(
            ContractApiDialogues, self.context.contract_api_dialogues
        )
        contract_api_msg, contract_api_dialogue = contract_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=ContractApiMessage.Performative.GET_RAW_TRANSACTION,
            ledger_id=strategy.ledger_id,
            contract_id="eightballer/sushi_farm:0.1.0",
            contract_address=strategy.reward_contract_address,
            callable="harvest",
            kwargs=ContractApiMessage.Kwargs(
                {"pid": pid, "address": self.context.agent_address}
            ),

        )
        contract_api_dialogue.terms = strategy.get_deploy_terms()
        self.context.outbox.put_message(message=contract_api_msg)
        strategy.transacting = True
        strategy.pending_sushi_pools[pid] = 0

    def teardown(self) -> None:
        """Implement the task teardown."""
        self.log(f"SushiFarmer teardown..")
