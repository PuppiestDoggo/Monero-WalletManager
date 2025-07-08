from fastapi import FastAPI

from WalletManager.Monero.walletManager import router as wallet_router
app = FastAPI()
app.include_router(wallet_router)

