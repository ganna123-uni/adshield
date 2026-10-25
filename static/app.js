"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const result = document.getElementById("result");
    const eventsList = document.getElementById("events");

    async function refreshDashboard() {
        try {
            const response = await fetch("/dashboard");

            if (!response.ok) {
                throw new Error("Could not load dashboard");
            }

            const data = await response.json();

            document.getElementById("total").textContent = data.total_events;
            document.getElementById("allowed").textContent = data.allowed;
            document.getElementById("blocked").textContent = data.blocked;

            eventsList.replaceChildren();

            if (data.recent_events.length === 0) {
                const item = document.createElement("li");
                item.textContent = "No events yet.";
                eventsList.appendChild(item);
                return;
            }

            data.recent_events.forEach(event => {
                const item = document.createElement("li");
                item.textContent =
                    `${event.timestamp} | ${event.decision} | ${event.reason}`;
                eventsList.appendChild(item);
            });
        } catch (error) {
            result.textContent = "Dashboard error: " + error.message;
        }
    }

    document.querySelectorAll("button[data-scenario]").forEach(button => {
        button.addEventListener("click", async () => {
            result.textContent = "Running security test...";

            try {
                const response = await fetch("/simulate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        scenario: button.dataset.scenario
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Test failed");
                }

                result.textContent =
                    `Decision: ${data.decision} — ${data.reason}`;

                await refreshDashboard();
            } catch (error) {
                result.textContent = "Error: " + error.message;
            }
        });
    });

    document.getElementById("refresh").addEventListener(
        "click",
        refreshDashboard
    );

    refreshDashboard();
});
