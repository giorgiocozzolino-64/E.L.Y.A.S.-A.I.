/*
E.L.Y.A.S.-A.I. Market Execution Engine v1
-----------------------------------------
Frontend execution + matching simulator.

Upload to:
assets/js/market-engine.js

Purpose:
- Create BUY / SELL orders
- Store orders locally with localStorage
- Match BUY >= SELL automatically
- Generate trade history
- Dispatch realtime events for UI pages
- Prepare architecture for backend matching engine

Events:
- elyas:ordersUpdated
- elyas:tradesUpdated
- elyas:orderMatched
*/

(function () {
    const STORAGE_ORDERS = "elyas_orders_v1";
    const STORAGE_TRADES = "elyas_trades_v1";
    const ENGINE_VERSION = "1.0.0";

    function uid(prefix) {
        return prefix + "-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).slice(2, 7).toUpperCase();
    }

    function nowIso() {
        return new Date().toISOString();
    }

    function money(v) {
        return "£" + Number(v || 0).toLocaleString("en-GB");
    }

    function readJson(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function writeJson(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    }

    function getOrders() {
        return readJson(STORAGE_ORDERS, []);
    }

    function saveOrders(orders) {
        writeJson(STORAGE_ORDERS, orders);
        window.dispatchEvent(new CustomEvent("elyas:ordersUpdated", {
            detail: getSnapshot()
        }));
    }

    function getTrades() {
        return readJson(STORAGE_TRADES, []);
    }

    function saveTrades(trades) {
        writeJson(STORAGE_TRADES, trades);
        window.dispatchEvent(new CustomEvent("elyas:tradesUpdated", {
            detail: getSnapshot()
        }));
    }

    function seedIfEmpty() {
        const existing = getOrders();

        if (existing.length > 0) return;

        const seedOrders = [
            createOrderObject({
                side: "BUY",
                symbol: "CASK-1",
                assetName: "Ardbeg 2023 Oloroso",
                price: 43800,
                quantity: 1,
                owner: "Investor Desk"
            }),
            createOrderObject({
                side: "BUY",
                symbol: "CASK-1",
                assetName: "Ardbeg 2023 Oloroso",
                price: 43100,
                quantity: 2,
                owner: "Broker Pool"
            }),
            createOrderObject({
                side: "SELL",
                symbol: "CASK-1",
                assetName: "Ardbeg 2023 Oloroso",
                price: 46200,
                quantity: 1,
                owner: "Private Seller"
            }),
            createOrderObject({
                side: "SELL",
                symbol: "CASK-1",
                assetName: "Ardbeg 2023 Oloroso",
                price: 47500,
                quantity: 1,
                owner: "Distillery Partner"
            }),
            createOrderObject({
                side: "BUY",
                symbol: "CASK-2",
                assetName: "Macallan 2022 Sherry Butt",
                price: 88900,
                quantity: 1,
                owner: "Institutional Buyer"
            }),
            createOrderObject({
                side: "SELL",
                symbol: "CASK-2",
                assetName: "Macallan 2022 Sherry Butt",
                price: 94300,
                quantity: 1,
                owner: "Broker Desk"
            })
        ];

        saveOrders(seedOrders);
    }

    function createOrderObject(input) {
        return {
            id: uid("ORD"),
            side: String(input.side || "BUY").toUpperCase(),
            symbol: String(input.symbol || "UNKNOWN").toUpperCase(),
            assetName: input.assetName || input.title || "Unknown Asset",
            price: Number(input.price || 0),
            quantity: Number(input.quantity || 1),
            remainingQuantity: Number(input.quantity || 1),
            status: "OPEN",
            owner: input.owner || "Current User",
            createdAt: nowIso(),
            updatedAt: nowIso()
        };
    }

    function placeOrder(input) {
        const order = createOrderObject(input);

        if (!["BUY", "SELL"].includes(order.side)) {
            throw new Error("Invalid order side");
        }

        if (!order.price || order.price <= 0) {
            throw new Error("Invalid order price");
        }

        if (!order.quantity || order.quantity <= 0) {
            throw new Error("Invalid order quantity");
        }

        const orders = getOrders();
        orders.unshift(order);
        saveOrders(orders);

        const matchResult = matchSymbol(order.symbol);

        return {
            order,
            matchResult,
            snapshot: getSnapshot()
        };
    }

    function cancelOrder(orderId) {
        const orders = getOrders().map(order => {
            if (order.id === orderId && order.status === "OPEN") {
                return {
                    ...order,
                    status: "CANCELLED",
                    updatedAt: nowIso()
                };
            }
            return order;
        });

        saveOrders(orders);

        return getSnapshot();
    }

    function matchSymbol(symbol) {
        let orders = getOrders();
        let trades = getTrades();

        let matchedTrades = [];

        let openBuys = orders
            .filter(o => o.symbol === symbol && o.side === "BUY" && o.status === "OPEN" && o.remainingQuantity > 0)
            .sort((a, b) => b.price - a.price || new Date(a.createdAt) - new Date(b.createdAt));

        let openSells = orders
            .filter(o => o.symbol === symbol && o.side === "SELL" && o.status === "OPEN" && o.remainingQuantity > 0)
            .sort((a, b) => a.price - b.price || new Date(a.createdAt) - new Date(b.createdAt));

        while (openBuys.length > 0 && openSells.length > 0) {
            const buy = openBuys[0];
            const sell = openSells[0];

            if (buy.price < sell.price) {
                break;
            }

            const qty = Math.min(buy.remainingQuantity, sell.remainingQuantity);
            const executionPrice = Math.round((buy.price + sell.price) / 2);

            const trade = {
                id: uid("TRD"),
                symbol,
                assetName: buy.assetName || sell.assetName,
                price: executionPrice,
                quantity: qty,
                buyerOrderId: buy.id,
                sellerOrderId: sell.id,
                buyer: buy.owner,
                seller: sell.owner,
                createdAt: nowIso(),
                status: "COMPLETED"
            };

            matchedTrades.unshift(trade);
            trades.unshift(trade);

            buy.remainingQuantity -= qty;
            sell.remainingQuantity -= qty;

            if (buy.remainingQuantity <= 0) {
                buy.status = "FILLED";
                buy.updatedAt = nowIso();
                openBuys.shift();
            } else {
                buy.status = "PARTIAL";
                buy.updatedAt = nowIso();
            }

            if (sell.remainingQuantity <= 0) {
                sell.status = "FILLED";
                sell.updatedAt = nowIso();
                openSells.shift();
            } else {
                sell.status = "PARTIAL";
                sell.updatedAt = nowIso();
            }
        }

        const byId = {};
        orders.forEach(o => byId[o.id] = o);

        openBuys.concat(openSells).forEach(o => {
            byId[o.id] = o;
        });

        orders = orders.map(o => byId[o.id] || o);

        saveOrders(orders);
        saveTrades(trades.slice(0, 100));

        if (matchedTrades.length > 0) {
            window.dispatchEvent(new CustomEvent("elyas:orderMatched", {
                detail: {
                    symbol,
                    trades: matchedTrades,
                    snapshot: getSnapshot()
                }
            }));
        }

        return matchedTrades;
    }

    function getOrderBook(symbol) {
        const orders = getOrders()
            .filter(o => o.symbol === symbol && o.status === "OPEN" && o.remainingQuantity > 0);

        const bids = orders
            .filter(o => o.side === "BUY")
            .sort((a, b) => b.price - a.price)
            .slice(0, 12);

        const asks = orders
            .filter(o => o.side === "SELL")
            .sort((a, b) => a.price - b.price)
            .slice(0, 12);

        const bestBid = bids[0]?.price || 0;
        const bestAsk = asks[0]?.price || 0;
        const spread = bestAsk && bestBid ? bestAsk - bestBid : 0;
        const mid = bestAsk && bestBid ? Math.round((bestAsk + bestBid) / 2) : 0;

        return {
            symbol,
            bids,
            asks,
            bestBid,
            bestAsk,
            spread,
            mid
        };
    }

    function getSymbols() {
        const orders = getOrders();
        const symbols = [...new Set(orders.map(o => o.symbol))];

        return symbols.map(symbol => {
            const first = orders.find(o => o.symbol === symbol);
            return {
                symbol,
                assetName: first?.assetName || symbol
            };
        });
    }

    function getSnapshot() {
        const orders = getOrders();
        const trades = getTrades();

        return {
            version: ENGINE_VERSION,
            orders,
            trades,
            symbols: getSymbols(),
            generatedAt: nowIso()
        };
    }

    function clearEngine() {
        localStorage.removeItem(STORAGE_ORDERS);
        localStorage.removeItem(STORAGE_TRADES);
        seedIfEmpty();

        window.dispatchEvent(new CustomEvent("elyas:ordersUpdated", {
            detail: getSnapshot()
        }));

        window.dispatchEvent(new CustomEvent("elyas:tradesUpdated", {
            detail: getSnapshot()
        }));

        return getSnapshot();
    }

    function renderOrderBook(selector, symbol) {
        const target = document.querySelector(selector);
        if (!target) return;

        const book = getOrderBook(symbol);

        const asksHtml = book.asks.map(order => `
            <div class="engine-row ask">
                <span>ASK</span>
                <span>${money(order.price)}</span>
                <span>${order.remainingQuantity}</span>
            </div>
        `).join("");

        const bidsHtml = book.bids.map(order => `
            <div class="engine-row bid">
                <span>BID</span>
                <span>${money(order.price)}</span>
                <span>${order.remainingQuantity}</span>
            </div>
        `).join("");

        target.innerHTML = `
            <div class="engine-book">
                <div class="engine-book-title">${symbol} Order Book</div>
                <div class="engine-book-meta">
                    Best Bid: ${money(book.bestBid)} · Best Ask: ${money(book.bestAsk)} · Spread: ${money(book.spread)}
                </div>
                <div class="engine-book-grid">
                    <div>
                        <div class="engine-col-title">ASKS</div>
                        ${asksHtml || "<div class='engine-empty'>No asks</div>"}
                    </div>
                    <div>
                        <div class="engine-col-title">BIDS</div>
                        ${bidsHtml || "<div class='engine-empty'>No bids</div>"}
                    </div>
                </div>
            </div>
        `;
    }

    function renderTrades(selector) {
        const target = document.querySelector(selector);
        if (!target) return;

        const trades = getTrades();

        if (!trades.length) {
            target.innerHTML = "<div class='engine-empty'>No executed trades yet.</div>";
            return;
        }

        target.innerHTML = trades.slice(0, 12).map(trade => `
            <div class="engine-trade-row">
                <span>${new Date(trade.createdAt).toLocaleTimeString("en-GB")}</span>
                <span>${trade.symbol}</span>
                <span>${trade.quantity}</span>
                <span>${money(trade.price)}</span>
            </div>
        `).join("");
    }

    window.ELYASMarketExecution = {
        version: ENGINE_VERSION,
        placeOrder,
        cancelOrder,
        matchSymbol,
        getOrderBook,
        getOrders,
        getTrades,
        getSymbols,
        getSnapshot,
        clearEngine,
        renderOrderBook,
        renderTrades,
        money
    };

    document.addEventListener("DOMContentLoaded", function () {
        seedIfEmpty();

        window.dispatchEvent(new CustomEvent("elyas:executionReady", {
            detail: getSnapshot()
        }));
    });
})();
