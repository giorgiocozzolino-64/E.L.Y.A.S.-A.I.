/*
E.L.Y.A.S.-A.I. Live Market Engine v1
------------------------------------
Frontend realtime simulation module.

Purpose:
- Simulate WebSocket-style live market updates.
- Keep the current backend API untouched.
- Prepare frontend architecture for a real WebSocket backend later.

How to use:
1. Upload this file to:
   assets/js/market-socket.js

2. Add before </body>:
   <script src="assets/js/market-socket.js"></script>

3. Optional listeners:
   window.addEventListener("elyas:marketTick", function(event) {
       console.log(event.detail);
   });
*/

(function () {
    const ENGINE_VERSION = "1.0.0";

    const state = {
        connected: false,
        tick: 0,
        markets: {
            islayCaskIndex: 1284.5,
            rareBottleIndex: 2412.0,
            sherryOakPremium: 918.2,
            distilleryDirectSales: 82400,
            volume24h: 842000,
            avgSpread: 3.8
        },
        assets: [
            {
                symbol: "ARDBEG-23",
                name: "Ardbeg 2023 Oloroso",
                assetType: "cask",
                price: 45200,
                previousPrice: 45200,
                bid: 43680,
                ask: 46330,
                volume: 3,
                signal: "Bullish"
            },
            {
                symbol: "MACALLAN-22",
                name: "Macallan 2022 Sherry Butt",
                assetType: "cask",
                price: 92000,
                previousPrice: 92000,
                bid: 88950,
                ask: 94300,
                volume: 1,
                signal: "Institutional Demand"
            },
            {
                symbol: "BUNNA-24",
                name: "Bunnahabhain 2024 Ex-Bourbon",
                assetType: "cask",
                price: 38500,
                previousPrice: 38500,
                bid: 37150,
                ask: 39550,
                volume: 4,
                signal: "Stable"
            },
            {
                symbol: "LAPH-25",
                name: "Laphroaig 2025 Quarter Cask",
                assetType: "cask",
                price: 41000,
                previousPrice: 41000,
                bid: 39700,
                ask: 42150,
                volume: 2,
                signal: "Low Volatility"
            },
            {
                symbol: "RARE-1998",
                name: "Single Cask Release 1998",
                assetType: "bottle",
                price: 2800,
                previousPrice: 2800,
                bid: 2680,
                ask: 2910,
                volume: 8,
                signal: "Collector Demand"
            }
        ],
        trades: []
    };

    function randomBetween(min, max) {
        return Math.random() * (max - min) + min;
    }

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function money(value) {
        return "£" + Number(value || 0).toLocaleString("en-GB");
    }

    function updateAsset(asset) {
        asset.previousPrice = asset.price;

        const volatility = asset.assetType === "bottle" ? 0.018 : 0.010;
        const drift = randomBetween(-volatility, volatility);
        const nextPrice = Math.round(asset.price * (1 + drift));

        asset.price = Math.max(100, nextPrice);
        asset.bid = Math.round(asset.price * randomBetween(0.955, 0.982));
        asset.ask = Math.round(asset.price * randomBetween(1.012, 1.038));
        asset.volume = Math.max(1, Math.round(asset.volume + randomBetween(-1, 2)));

        const changePct = ((asset.price - asset.previousPrice) / asset.previousPrice) * 100;

        if (changePct > 0.8) asset.signal = "Bullish";
        else if (changePct < -0.8) asset.signal = "Bearish";
        else if (asset.assetType === "bottle") asset.signal = "Collector Demand";
        else asset.signal = "Stable";
    }

    function updateMarkets() {
        state.markets.islayCaskIndex = clamp(
            state.markets.islayCaskIndex + randomBetween(-5.5, 6.5),
            900,
            1800
        );

        state.markets.rareBottleIndex = clamp(
            state.markets.rareBottleIndex + randomBetween(-9, 10),
            1800,
            3200
        );

        state.markets.sherryOakPremium = clamp(
            state.markets.sherryOakPremium + randomBetween(-4, 5),
            650,
            1200
        );

        state.markets.volume24h = clamp(
            state.markets.volume24h + randomBetween(-24000, 36000),
            250000,
            2500000
        );

        state.markets.avgSpread = clamp(
            state.markets.avgSpread + randomBetween(-0.18, 0.22),
            2.2,
            6.8
        );

        state.markets.distilleryDirectSales = clamp(
            state.markets.distilleryDirectSales + randomBetween(-1800, 2600),
            30000,
            220000
        );
    }

    function generateTrade() {
        const asset = state.assets[Math.floor(Math.random() * state.assets.length)];
        const trade = {
            id: "TRD-" + String(Date.now()).slice(-7),
            symbol: asset.symbol,
            name: asset.name,
            price: asset.price,
            amount: asset.price,
            quantity: Math.max(1, Math.round(randomBetween(1, 3))),
            side: Math.random() > 0.5 ? "BUY" : "SELL",
            time: new Date().toLocaleTimeString("en-GB"),
            signal: asset.signal
        };

        state.trades.unshift(trade);
        state.trades = state.trades.slice(0, 12);
    }

    function tick() {
        state.tick += 1;
        updateMarkets();

        state.assets.forEach(updateAsset);

        if (Math.random() > 0.25) {
            generateTrade();
        }

        const snapshot = getSnapshot();

        window.dispatchEvent(new CustomEvent("elyas:marketTick", {
            detail: snapshot
        }));

        renderAutoBoundElements(snapshot);
    }

    function getSnapshot() {
        return JSON.parse(JSON.stringify({
            version: ENGINE_VERSION,
            connected: state.connected,
            tick: state.tick,
            timestamp: new Date().toISOString(),
            markets: state.markets,
            assets: state.assets,
            trades: state.trades
        }));
    }

    function renderAutoBoundElements(snapshot) {
        setText("[data-elyas-market-status]", snapshot.connected ? "LIVE" : "OFFLINE");
        setText("[data-elyas-clock]", new Date().toLocaleTimeString("en-GB"));

        setText("[data-elyas-islay-index]", snapshot.markets.islayCaskIndex.toFixed(1));
        setText("[data-elyas-bottle-index]", snapshot.markets.rareBottleIndex.toFixed(1));
        setText("[data-elyas-sherry-index]", snapshot.markets.sherryOakPremium.toFixed(1));
        setText("[data-elyas-volume]", money(snapshot.markets.volume24h));
        setText("[data-elyas-spread]", snapshot.markets.avgSpread.toFixed(1) + "%");

        const totalPortfolio = snapshot.assets
            .filter(a => a.assetType === "cask")
            .reduce((sum, a) => sum + a.price, 0);

        setText("[data-elyas-live-portfolio]", money(totalPortfolio));

        renderTickerTape(snapshot);
        renderTradesFeed(snapshot);
    }

    function setText(selector, value) {
        document.querySelectorAll(selector).forEach(el => {
            el.textContent = value;
        });
    }

    function renderTickerTape(snapshot) {
        document.querySelectorAll("[data-elyas-ticker-tape]").forEach(el => {
            el.innerHTML = snapshot.assets.map(asset => {
                const change = asset.price - asset.previousPrice;
                const cls = change >= 0 ? "positive" : "negative";
                const arrow = change >= 0 ? "▲" : "▼";
                const pct = asset.previousPrice
                    ? ((change / asset.previousPrice) * 100).toFixed(2)
                    : "0.00";

                return `
                    <span class="ticker-item">
                        <b>${asset.symbol}</b>
                        ${money(asset.price)}
                        <span class="${cls}">${arrow} ${pct}%</span>
                    </span>
                `;
            }).join("");
        });
    }

    function renderTradesFeed(snapshot) {
        document.querySelectorAll("[data-elyas-trades-feed]").forEach(el => {
            if (!snapshot.trades.length) {
                el.innerHTML = "<div class='trade-feed-row'>Waiting for trades...</div>";
                return;
            }

            el.innerHTML = snapshot.trades.slice(0, 8).map(trade => {
                const cls = trade.side === "BUY" ? "positive" : "negative";
                return `
                    <div class="trade-feed-row">
                        <span>${trade.time}</span>
                        <span>${trade.symbol}</span>
                        <span class="${cls}">${trade.side}</span>
                        <span>${money(trade.price)}</span>
                    </div>
                `;
            }).join("");
        });
    }

    function connect() {
        if (state.connected) return;

        state.connected = true;

        window.dispatchEvent(new CustomEvent("elyas:marketConnected", {
            detail: getSnapshot()
        }));

        tick();

        setInterval(tick, 2500);
    }

    window.ELYASMarketEngine = {
        connect,
        getSnapshot,
        money,
        version: ENGINE_VERSION
    };

    document.addEventListener("DOMContentLoaded", function () {
        connect();
    });
})();
