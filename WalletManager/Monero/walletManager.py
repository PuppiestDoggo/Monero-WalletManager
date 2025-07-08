from fastapi import APIRouter
from WalletManager.Monero.RpcManager import WalletRPC
from pydantic import BaseModel
router = APIRouter()
w = WalletRPC()

class TransferRequest(BaseModel):
    subaddr_index: int       # was subaddressID
    dest_address: str        # was dest_id
    amount: float
    priority: int

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/accounts/")
async def accounts():
    return w.list_subaddresses()

@router.get("/create_address/{label}")
async def create_address(label: str):
    return w.create_address(label=label)

@router.get("/address/by_label/{label}")
async def create_address(label: str):
    for i in w.list_subaddresses():
        if i["label"] == label:
            return i
    return "Nope"

@router.get("/address/by_address/{address}")
async def create_address(address: str):
    for i in w.list_subaddresses():
        if i["address"] == address:
            return i
    return "Nope"

@router.get("/get_balance/{address}")
async def get_balance(address: int):
    return w.get_balance(address)

@router.post("/transfer")
async def transfer(req: TransferRequest):
    return w.transfer(req.subaddr_index, req.dest_address, req.amount, req.priority)
