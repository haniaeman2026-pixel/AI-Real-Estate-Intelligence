/* =========================================================
   AI REAL ESTATE INTELLIGENCE PLATFORM
   COMPLETE FRONTEND CONTROLLER
========================================================= */

let mapInstance = null;
let mapInitialized = false;

let savedProperties = [];


/* =========================================================
   START APPLICATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    loadSavedProperties();

    initializeIcons();

    initializeNavigation();

    initializePrediction();

    initializeRecommendations();

    initializeChat();

    initializeRAG();

    initializeQuickAsk();

    initializeGlobalSearch();

    initializeNotifications();

    initializeTheme();

    initializeSavedProperties();

    initializeMap();

    loadHealthStatus();

    const initialView =
        window.location.hash
            ? window.location.hash.substring(1)
            : "dashboard";

    showView(
        isValidView(initialView)
            ? initialView
            : "dashboard",
        false
    );

});


/* =========================================================
   VALID VIEWS
========================================================= */

function isValidView(view) {

    return [
        "dashboard",
        "prediction",
        "recommendations",
        "assistant",
        "knowledge",
        "market",
        "map",
        "saved",
        "settings"
    ].includes(view);

}


/* =========================================================
   ICONS
========================================================= */

function initializeIcons() {

    if (
        typeof lucide !== "undefined"
    ) {

        lucide.createIcons();

    }

}


function refreshIcons() {

    initializeIcons();

}


/* =========================================================
   TOAST
========================================================= */

function showToast(message) {

    const toast =
        document.getElementById("toast");

    const toastMessage =
        document.getElementById("toastMessage");


    if (!toast || !toastMessage) {
        return;
    }


    toastMessage.textContent =
        message;


    toast.classList.add("show");


    clearTimeout(
        window.toastTimeout
    );


    window.toastTimeout =
        setTimeout(() => {

            toast.classList.remove(
                "show"
            );

        }, 3000);

}


/* =========================================================
   NAVIGATION
========================================================= */

function initializeNavigation() {

    document
        .querySelectorAll(
            ".nav-item[data-target]"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    showView(
                        button.dataset.target
                    );

                }
            );

        });


    const savedButton =
        document.getElementById(
            "savedBtn"
        );


    if (savedButton) {

        savedButton.addEventListener(
            "click",
            () => {

                showView("saved");

            }
        );

    }


    const settingsButton =
        document.getElementById(
            "settingsBtn"
        );


    if (settingsButton) {

        settingsButton.addEventListener(
            "click",
            () => {

                showView("settings");

            }
        );

    }

}


/* =========================================================
   VIEW CONTROLLER
========================================================= */

function showView(
    view,
    updateURL = true
) {

    if (!isValidView(view)) {

        view = "dashboard";

    }


    const content =
        document.getElementById(
            "dashboard"
        );


    if (!content) {
        return;
    }


    /*
       Existing UI sections
    */

    const hero =
        content.querySelector(
            ".hero-grid"
        );

    const featureGrid =
        content.querySelector(
            ".feature-grid"
        );

    const dashboardGrid =
        content.querySelector(
            ".dashboard-grid"
        );

    const quickAsk =
        content.querySelector(
            ".quick-ask"
        );

    const prediction =
        document.getElementById(
            "prediction"
        );

    const recommendations =
        document.getElementById(
            "recommendations"
        );

    const assistant =
        document.getElementById(
            "assistant"
        );

    const knowledge =
        document.getElementById(
            "knowledge"
        );

    const market =
        document.getElementById(
            "market"
        );

    const saved =
        document.getElementById(
            "savedView"
        );

    const settings =
        document.getElementById(
            "settingsView"
        );


    /*
       Dashboard right-side components
    */

    const rightColumn =
        content.querySelector(
            ".right-column"
        );

    const locationPanel =
        content.querySelector(
            ".location-panel"
        );


    /*
       Hide everything first
    */

    [
        hero,
        featureGrid,
        dashboardGrid,
        quickAsk,
        prediction,
        recommendations,
        assistant,
        knowledge,
        market,
        saved,
        settings,
        rightColumn,
        locationPanel
    ]
        .filter(Boolean)
        .forEach(element => {

            element.style.display =
                "none";

        });


    /*
       DASHBOARD
    */

    if (view === "dashboard") {

        if (hero) {

            hero.style.display =
                "";

        }


        if (featureGrid) {

            featureGrid.style.display =
                "";

        }


        if (dashboardGrid) {

            dashboardGrid.style.display =
                "grid";

        }


        if (prediction) {

            prediction.style.display =
                "";

        }


        if (recommendations) {

            recommendations.style.display =
                "";

        }


        if (rightColumn) {

            rightColumn.style.display =
                "";

        }


        if (locationPanel) {

            locationPanel.style.display =
                "";

        }


        if (market) {

            market.style.display =
                "";

        }


        if (assistant) {

            assistant.style.display =
                "";

        }


        if (knowledge) {

            knowledge.style.display =
                "";

        }


        if (quickAsk) {

            quickAsk.style.display =
                "";

        }

    }


    /*
       PREDICTION
    */

    else if (view === "prediction") {

        if (dashboardGrid) {

            dashboardGrid.style.display =
                "grid";

            dashboardGrid.style.gridTemplateColumns =
                "1fr";

        }


        if (prediction) {

            prediction.style.display =
                "block";

        }

    }


    /*
       RECOMMENDATIONS
    */

    else if (
        view === "recommendations"
    ) {

        if (dashboardGrid) {

            dashboardGrid.style.display =
                "grid";

            dashboardGrid.style.gridTemplateColumns =
                "1fr";

        }


        if (recommendations) {

            recommendations.style.display =
                "block";

        }


        loadRecommendations();

    }


    /*
       AI ASSISTANT
    */

    else if (view === "assistant") {

        if (assistant) {

            assistant.style.display =
                "block";

        }

    }


    /*
       RAG
    */

    else if (view === "knowledge") {

        if (knowledge) {

            knowledge.style.display =
                "block";

        }

    }


    /*
       MARKET
    */

    else if (view === "market") {

        if (dashboardGrid) {

            dashboardGrid.style.display =
                "grid";

            dashboardGrid.style.gridTemplateColumns =
                "1fr";

        }


        if (market) {

            market.style.display =
                "block";

        }


        loadMarketInsights();

    }


    /*
       MAP
    */

    else if (view === "map") {

        if (dashboardGrid) {

            dashboardGrid.style.display =
                "grid";

            dashboardGrid.style.gridTemplateColumns =
                "1fr";

        }


        if (locationPanel) {

            locationPanel.style.display =
                "block";

        }


        setTimeout(() => {

            initializeMap();

            if (mapInstance) {

                mapInstance.invalidateSize();

            }

        }, 150);

    }


    /*
       SAVED
    */

    else if (view === "saved") {

        if (saved) {

            saved.style.display =
                "block";

        }


        renderSavedProperties();

    }


    /*
       SETTINGS
    */

    else if (view === "settings") {

        if (settings) {

            settings.style.display =
                "block";

        }


        checkSettingsAPI();

    }


    /*
       Active navigation
    */

    document
        .querySelectorAll(
            ".nav-item"
        )
        .forEach(item => {

            item.classList.remove(
                "active"
            );

        });


    const activeItem =
        document.querySelector(
            `.nav-item[data-target="${view}"]`
        );


    if (activeItem) {

        activeItem.classList.add(
            "active"
        );

    }


    /*
       URL
    */

    if (updateURL) {

        history.pushState(
            { view: view },
            "",
            "#" + view
        );

    }


    /*
       Special actions
    */

    if (view === "map") {

        setTimeout(() => {

            initializeMap();

            if (mapInstance) {

                mapInstance.invalidateSize();

            }

        }, 200);

    }


    refreshIcons();


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


/* =========================================================
   QUICK NAVIGATION
========================================================= */

function scrollToSection(id) {

    showView(id);

}


window.scrollToSection =
    scrollToSection;


/* =========================================================
   BROWSER BACK/FORWARD
========================================================= */

window.addEventListener(
    "popstate",
    () => {

        const view =
            location.hash.substring(1)
            || "dashboard";


        showView(
            view,
            false
        );

    }
);


/* =========================================================
   PRICE PREDICTION
========================================================= */

function initializePrediction() {

    const form =
        document.getElementById(
            "predictionForm"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const button =
                form.querySelector(
                    "button[type='submit']"
                );


            const originalHTML =
                button.innerHTML;


            button.disabled =
                true;


            button.innerHTML =
                `
                <span class="loading-spinner"></span>
                Predicting...
                `;


            const payload = {

                overall_qual:
                    Number(
                        document.getElementById(
                            "overallQual"
                        ).value
                    ),

                gr_liv_area:
                    Number(
                        document.getElementById(
                            "grLivArea"
                        ).value
                    ),

                year_built:
                    Number(
                        document.getElementById(
                            "yearBuilt"
                        ).value
                    ),

                total_bsmt_sf:
                    Number(
                        document.getElementById(
                            "totalBsmtSf"
                        ).value
                    ),

                garage_cars:
                    Number(
                        document.getElementById(
                            "garageCars"
                        ).value
                    ),

                full_bath:
                    Number(
                        document.getElementById(
                            "fullBath"
                        ).value
                    ),

                bedroom_abv_gr:
                    Number(
                        document.getElementById(
                            "bedroomAbvGr"
                        ).value
                    ),

                lot_area:
                    Number(
                        document.getElementById(
                            "lotArea"
                        ).value
                    ),

                neighborhood:
                    document.getElementById(
                        "neighborhood"
                    ).value

            };


            try {

                const response =
                    await fetch(
                        "/api/prediction/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Prediction failed."
                    );

                }


                const price =
                    data.predicted_price ??
                    data.predictedPrice ??
                    data.price ??
                    data.prediction;


                const result =
                    document.getElementById(
                        "predictionResult"
                    );


                if (
                    result &&
                    price !== undefined
                ) {

                    result.textContent =
                        formatCurrency(
                            price
                        );

                }


                showToast(
                    "Property price predicted successfully."
                );


            } catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );


                showToast(
                    error.message ||
                    "Prediction failed."
                );

            }


            button.disabled =
                false;


            button.innerHTML =
                originalHTML;


            refreshIcons();

        }
    );

}


/* =========================================================
   CURRENCY FORMAT
========================================================= */

function formatCurrency(value) {

    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return "$0";

    }


    return new Intl.NumberFormat(
        "en-US",
        {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0
        }
    ).format(number);

}


/* =========================================================
   RECOMMENDATIONS
========================================================= */

function initializeRecommendations() {

    const list =
        document.getElementById(
            "recommendationList"
        );


    if (!list) {
        return;
    }


    list.addEventListener(
        "click",
        event => {

            const heart =
                event.target.closest(
                    ".heart-btn"
                );


            if (!heart) {
                return;
            }


            saveProperty(
                heart.closest(
                    ".property-item"
                ),
                heart
            );

        }
    );

}


async function loadRecommendations() {

    const list =
        document.getElementById(
            "recommendationList"
        );


    if (!list) {
        return;
    }


    list.innerHTML =
        `
        <div class="loading-state">
            Finding the best matching properties...
        </div>
        `;


    /*
       Demo defaults.
       These can be connected to your
       recommendation form if you have one.
    */

    const payload = {

        budget: 400000,

        bedrooms: 3,

        neighborhood: "",

        min_area: 1200,

        top_k: 6

    };


    try {

        const response =
            await fetch(
                "/api/recommendation/recommend",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Recommendation service failed."
            );

        }


        const properties =
            data.recommendations ||
            data.results ||
            data.properties ||
            data;


        if (
            !Array.isArray(
                properties
            ) ||
            properties.length === 0
        ) {

            list.innerHTML =
                `
                <div class="loading-state">
                    No matching properties found.
                </div>
                `;

            return;

        }


        renderRecommendations(
            properties
        );


    } catch (error) {

        console.error(
            "Recommendation error:",
            error
        );


        list.innerHTML =
            `
            <div class="loading-state">
                Unable to load recommendations.
            </div>
            `;


        showToast(
            "Recommendation service is unavailable."
        );

    }

}


/* =========================================================
   RENDER RECOMMENDATIONS
========================================================= */

function renderRecommendations(
    properties
) {

    const list =
        document.getElementById(
            "recommendationList"
        );


    list.innerHTML = "";


    properties
        .slice(0, 6)
        .forEach(
            (property, index) => {

                const price =
                    property.price ??
                    property.sale_price ??
                    property.SalePrice ??
                    0;


                const bedrooms =
                    property.bedrooms ??
                    property.BedroomAbvGr ??
                    0;


                const area =
                    property.area ??
                    property.gr_liv_area ??
                    property.GrLivArea ??
                    0;


                const neighborhood =
                    property.neighborhood ??
                    property.Neighborhood ??
                    "Unknown";


                const year =
                    property.year_built ??
                    property.YearBuilt ??
                    "—";


                const bathrooms =
                    property.bathrooms ??
                    property.FullBath ??
                    0;


                const garage =
                    property.garage_cars ??
                    property.GarageCars ??
                    0;


                const score =
                    property.recommendation_score ??
                    property.score ??
                    "";


                const labels = [
                    "Best Match",
                    "Great Value",
                    "Recommended",
                    "Good Option"
                ];


                const classes = [
                    "green-badge",
                    "blue-badge",
                    "purple-badge",
                    "orange-badge"
                ];


                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "property-item";


                item.dataset.price =
                    price;

                item.dataset.bedrooms =
                    bedrooms;

                item.dataset.area =
                    area;

                item.dataset.neighborhood =
                    neighborhood;

                item.dataset.year =
                    year;


                item.innerHTML =
                    `
                    <div class="property-image house-one"></div>

                    <div class="property-details">

                        <strong>
                            ${formatCurrency(price)}
                        </strong>

                        <span>
                            ${bedrooms} Beds ·
                            ${bathrooms} Baths ·
                            ${Number(area).toLocaleString()} sq ft
                        </span>

                        <small>
                            <i data-lucide="map-pin"></i>
                            ${escapeHTML(neighborhood)}
                        </small>

                        <small>
                            Built ${escapeHTML(year)}
                            ${garage ? ` · ${garage} Garage` : ""}
                        </small>

                        ${
                            score !== ""
                                ? `
                                <small>
                                    Match Score:
                                    ${Number(score).toFixed(1)}
                                </small>
                                `
                                : ""
                        }

                    </div>

                    <div class="property-badge ${classes[index % classes.length]}">
                        ${labels[index % labels.length]}
                    </div>

                    <button
                        type="button"
                        class="heart-btn"
                        aria-label="Save property"
                    >
                        ♡
                    </button>
                    `;


                list.appendChild(
                    item
                );

            }
        );


    markAlreadySaved();

    refreshIcons();

}


/* =========================================================
   SAVED PROPERTIES
========================================================= */

function loadSavedProperties() {

    try {

        savedProperties =
            JSON.parse(
                localStorage.getItem(
                    "realEstateSaved"
                )
            ) || [];

    } catch {

        savedProperties = [];

    }

}


function saveSavedProperties() {

    localStorage.setItem(
        "realEstateSaved",
        JSON.stringify(
            savedProperties
        )
    );

}


function saveProperty(
    element,
    button
) {

    if (!element) {
        return;
    }


    const property = {

        price:
            Number(
                element.dataset.price
            ),

        bedrooms:
            Number(
                element.dataset.bedrooms
            ),

        area:
            Number(
                element.dataset.area
            ),

        neighborhood:
            element.dataset.neighborhood,

        year:
            element.dataset.year

    };


    const index =
        savedProperties.findIndex(
            item =>
                item.price === property.price &&
                item.bedrooms === property.bedrooms &&
                item.area === property.area &&
                item.neighborhood ===
                    property.neighborhood
        );


    if (index >= 0) {

        savedProperties.splice(
            index,
            1
        );

        button.textContent =
            "♡";

        button.classList.remove(
            "saved"
        );

        showToast(
            "Property removed from saved."
        );

    } else {

        savedProperties.push(
            property
        );

        button.textContent =
            "♥";

        button.classList.add(
            "saved"
        );

        showToast(
            "Property saved."
        );

    }


    saveSavedProperties();

}


function markAlreadySaved() {

    document
        .querySelectorAll(
            ".property-item"
        )
        .forEach(item => {

            const exists =
                savedProperties.some(
                    saved =>
                        saved.price ===
                            Number(
                                item.dataset.price
                            ) &&
                        saved.bedrooms ===
                            Number(
                                item.dataset.bedrooms
                            ) &&
                        saved.area ===
                            Number(
                                item.dataset.area
                            ) &&
                        saved.neighborhood ===
                            item.dataset.neighborhood
                );


            if (exists) {

                const button =
                    item.querySelector(
                        ".heart-btn"
                    );


                if (button) {

                    button.textContent =
                        "♥";

                    button.classList.add(
                        "saved"
                    );

                }

            }

        });

}


function initializeSavedProperties() {

    const clear =
        document.getElementById(
            "clearSavedBtn"
        );


    if (clear) {

        clear.addEventListener(
            "click",
            () => {

                savedProperties = [];

                saveSavedProperties();

                renderSavedProperties();

                markAlreadySaved();

                showToast(
                    "Saved properties cleared."
                );

            }
        );

    }

}


function renderSavedProperties() {

    const container =
        document.getElementById(
            "savedPropertiesList"
        );


    if (!container) {
        return;
    }


    if (
        savedProperties.length === 0
    ) {

        container.innerHTML =
            `
            <div class="empty-saved">

                <i data-lucide="bookmark"></i>

                <strong>
                    No saved properties yet
                </strong>

                <span>
                    Save properties from Smart Recommendations.
                </span>

            </div>
            `;

        refreshIcons();

        return;

    }


    container.innerHTML = "";


    savedProperties.forEach(
        (property, index) => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "saved-property-item";


            item.innerHTML =
                `
                <div class="saved-property-icon">
                    ${index + 1}
                </div>

                <div>

                    <strong>
                        ${formatCurrency(property.price)}
                    </strong>

                    <span>
                        ${property.bedrooms} Beds ·
                        ${Number(property.area).toLocaleString()} sq ft
                    </span>

                    <small>
                        <i data-lucide="map-pin"></i>
                        ${escapeHTML(
                            property.neighborhood
                        )}
                    </small>

                </div>

                <button
                    type="button"
                    class="link-btn remove-saved"
                    data-index="${index}"
                >
                    Remove
                </button>
                `;


            container.appendChild(
                item
            );

        }
    );


    container
        .querySelectorAll(
            ".remove-saved"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const index =
                        Number(
                            button.dataset.index
                        );


                    savedProperties.splice(
                        index,
                        1
                    );


                    saveSavedProperties();

                    renderSavedProperties();

                    markAlreadySaved();

                }
            );

        });


    refreshIcons();

}


/* =========================================================
   AI CHAT
========================================================= */

function initializeChat() {

    const form =
        document.getElementById(
            "chatForm"
        );


    const input =
        document.getElementById(
            "chatMessage"
        );


    const windowElement =
        document.getElementById(
            "chatWindow"
        );


    if (
        !form ||
        !input ||
        !windowElement
    ) {

        return;

    }


    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const message =
                input.value.trim();


            if (!message) {
                return;
            }


            addChatMessage(
                message,
                "user"
            );


            input.value = "";


            const loadingId =
                addChatMessage(
                    "Thinking...",
                    "assistant"
                );


            try {

                const response =
                    await fetch(
                        "/api/chatbot/chat",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    message:
                                        message
                                })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "AI assistant failed."
                    );

                }


                removeChatMessage(
                    loadingId
                );


                addChatMessage(
                    data.answer ||
                    data.response ||
                    data.message ||
                    "No answer received.",
                    "assistant"
                );


            } catch (error) {

                console.error(
                    "Chat error:",
                    error
                );


                removeChatMessage(
                    loadingId
                );


                addChatMessage(
                    "The AI assistant could not respond. Please check your GROQ_API_KEY and backend.",
                    "assistant"
                );

            }

        }
    );

}


function addChatMessage(
    message,
    type
) {

    const chatWindow =
        document.getElementById(
            "chatWindow"
        );


    const wrapper =
        document.createElement(
            "div"
        );


    const id =
        "chat-" +
        Date.now() +
        "-" +
        Math.random()
            .toString(36)
            .substring(2);


    wrapper.id =
        id;


    wrapper.className =
        type === "user"
            ? "user-message"
            : "assistant-message";


    wrapper.innerHTML =
        `
        <div class="message-avatar">
            ${type === "user" ? "YOU" : "AI"}
        </div>

        <div class="message-bubble">
            ${escapeHTML(message)}
        </div>
        `;


    chatWindow.appendChild(
        wrapper
    );


    chatWindow.scrollTop =
        chatWindow.scrollHeight;


    return id;

}


function removeChatMessage(id) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.remove();

    }

}


/* =========================================================
   RAG
========================================================= */

function initializeRAG() {

    const form =
        document.getElementById(
            "ragForm"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const input =
                document.getElementById(
                    "ragQuestion"
                );


            const question =
                input.value.trim();


            if (!question) {
                return;
            }


            const result =
                document.getElementById(
                    "ragResult"
                );


            const answer =
                document.getElementById(
                    "ragAnswer"
                );


            const sources =
                document.getElementById(
                    "ragSources"
                );


            result.classList.remove(
                "hidden"
            );


            answer.textContent =
                "Searching the knowledge base...";


            sources.innerHTML = "";


            try {

                const response =
                    await fetch(
                        "/api/rag/ask",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    question:
                                        question
                                })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "RAG request failed."
                    );

                }


                answer.textContent =
                    data.answer ||
                    data.response ||
                    data.context ||
                    "No answer found.";


                const sourceList =
                    data.sources ||
                    data.documents ||
                    [];


                if (
                    Array.isArray(
                        sourceList
                    )
                ) {

                    sourceList.forEach(
                        source => {

                            const div =
                                document.createElement(
                                    "div"
                                );


                            div.className =
                                "source-item";


                            div.textContent =
                                typeof source ===
                                    "string"
                                    ? source
                                    : JSON.stringify(
                                        source
                                    );


                            sources.appendChild(
                                div
                            );

                        }
                    );

                }


                if (
                    sources.children.length === 0
                ) {

                    sources.innerHTML =
                        `
                        <div class="source-item">
                            Real estate knowledge base
                        </div>
                        `;

                }


                showToast(
                    "Knowledge search completed."
                );


                refreshIcons();

            } catch (error) {

                console.error(
                    "RAG error:",
                    error
                );


                answer.textContent =
                    "Unable to search the knowledge base. Please check the RAG service.";


                showToast(
                    "RAG service unavailable."
                );

            }

        }
    );

}


/* =========================================================
   QUICK ASK
========================================================= */

function initializeQuickAsk() {

    const form =
        document.getElementById(
            "quickAskForm"
        );


    const input =
        document.getElementById(
            "quickQuestion"
        );


    if (!form || !input) {
        return;
    }


    form.addEventListener(
        "submit",
        event => {

            event.preventDefault();


            const question =
                input.value.trim();


            if (!question) {
                return;
            }


            const chatInput =
                document.getElementById(
                    "chatMessage"
                );


            chatInput.value =
                question;


            showView(
                "assistant"
            );


            setTimeout(() => {

                document
                    .getElementById(
                        "chatForm"
                    )
                    ?.dispatchEvent(
                        new Event(
                            "submit",
                            {
                                bubbles: true,
                                cancelable: true
                            }
                        )
                    );

            }, 200);


            input.value = "";

        }
    );


    document
        .querySelectorAll(
            ".popular-questions button"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    input.value =
                        button.dataset.question ||
                        "";

                    input.focus();

                }
            );

        });

}


/* =========================================================
   GLOBAL SEARCH
========================================================= */

function initializeGlobalSearch() {

    const search =
        document.getElementById(
            "globalSearch"
        );


    if (!search) {
        return;
    }


    search.addEventListener(
        "keydown",
        event => {

            if (
                event.key !== "Enter"
            ) {

                return;

            }


            const query =
                search.value.trim();


            if (!query) {
                return;
            }


            const chatInput =
                document.getElementById(
                    "chatMessage"
                );


            if (chatInput) {

                chatInput.value =
                    query;

            }


            showView(
                "assistant"
            );


            setTimeout(() => {

                document
                    .getElementById(
                        "chatForm"
                    )
                    ?.dispatchEvent(
                        new Event(
                            "submit",
                            {
                                bubbles: true,
                                cancelable: true
                            }
                        )
                    );

            }, 200);


            search.value = "";

        }
    );

}


/* =========================================================
   REAL LEAFLET MAP
========================================================= */

function initializeMap() {

    const container =
        document.getElementById(
            "realMap"
        );


    if (
        !container ||
        typeof L === "undefined"
    ) {

        return;

    }


    if (
        mapInitialized &&
        mapInstance
    ) {

        mapInstance.invalidateSize();

        return;

    }


    mapInstance =
        L.map(
            container
        ).setView(
            [
                42.0347,
                -93.6200
            ],
            13
        );


    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,

            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(
        mapInstance
    );


    const locations = [

        {
            lat: 42.0466,
            lng: -93.6128,
            name: "North Ames"
        },

        {
            lat: 42.0194,
            lng: -93.6577,
            name: "West Ames"
        },

        {
            lat: 42.0308,
            lng: -93.6152,
            name: "NAmes"
        },

        {
            lat: 42.0276,
            lng: -93.6276,
            name: "Somerst"
        },

        {
            lat: 42.0217,
            lng: -93.6202,
            name: "OldTown"
        },

        {
            lat: 42.0056,
            lng: -93.6070,
            name: "StoneBr"
        }

    ];


    locations.forEach(
        location => {

            L.marker([
                location.lat,
                location.lng
            ])
            .addTo(
                mapInstance
            )
            .bindPopup(
                `
                <strong>
                    ${escapeHTML(
                        location.name
                    )}
                </strong>
                <br>
                Ames Housing Dataset neighborhood
                `
            );

        }
    );


    L.circle(
        [
            42.0347,
            -93.6200
        ],
        {
            radius: 1500,

            color: "#76553d",

            fillColor: "#c7a98b",

            fillOpacity: 0.12
        }
    )
    .addTo(
        mapInstance
    )
    .bindPopup(
        "Ames real estate analysis area"
    );


    mapInitialized =
        true;

}


/* =========================================================
   MARKET INSIGHTS
========================================================= */

async function loadMarketInsights() {

    try {

        const response =
            await fetch(
                "/api/market/insights"
            );


        if (!response.ok) {

            throw new Error(
                "Market API unavailable."
            );

        }


        const data =
            await response.json();


        /*
           Average price
        */

        const average =
            document.getElementById(
                "averagePrice"
            );


        if (
            average &&
            data.average_price !== undefined
        ) {

            average.textContent =
                formatCurrency(
                    data.average_price
                );

        }


        /*
           Trend cards
        */

        const cards =
            document.querySelectorAll(
                "#market .trend-card"
            );


        if (
            cards[0] &&
            data.average_price_per_sqft !==
                undefined
        ) {

            cards[0]
                .querySelector("strong")
                .textContent =
                formatCurrency(
                    data.average_price_per_sqft
                );

        }


        if (
            cards[1] &&
            data.average_property_age !==
                undefined
        ) {

            cards[1]
                .querySelector("strong")
                .textContent =
                `${Number(
                    data.average_property_age
                ).toFixed(1)} yrs`;

        }


        if (
            cards[2] &&
            data.average_living_area !==
                undefined
        ) {

            cards[2]
                .querySelector("strong")
                .textContent =
                `${Math.round(
                    data.average_living_area
                ).toLocaleString()} sq ft`;

        }


        if (
            cards[3] &&
            data.median_price !==
                undefined
        ) {

            cards[3]
                .querySelector("strong")
                .textContent =
                formatCurrency(
                    data.median_price
                );

        }


        showToast(
            "Market insights loaded."
        );


    } catch (error) {

        console.error(
            "Market error:",
            error
        );


        showToast(
            "Market insights API unavailable."
        );

    }

}


/* =========================================================
   HEALTH CHECK
========================================================= */

async function loadHealthStatus() {

    try {

        const response =
            await fetch(
                "/api/health"
            );


        if (!response.ok) {

            throw new Error();

        }


    } catch {

        showToast(
            "FastAPI is not reachable."
        );

    }

}


/* =========================================================
   SETTINGS API STATUS
========================================================= */

async function checkSettingsAPI() {

    const status =
        document.getElementById(
            "settingsApiStatus"
        );


    if (!status) {
        return;
    }


    status.textContent =
        "Checking...";


    try {

        const response =
            await fetch(
                "/api/health"
            );


        if (response.ok) {

            status.textContent =
                "Online";

            status.classList.remove(
                "bad"
            );

        } else {

            status.textContent =
                "Unavailable";

            status.classList.add(
                "bad"
            );

        }

    } catch {

        status.textContent =
            "Offline";

        status.classList.add(
            "bad"
        );

    }

}


/* =========================================================
   DARK MODE
========================================================= */

function initializeTheme() {

    const savedTheme =
        localStorage.getItem(
            "realEstateTheme"
        );


    if (
        savedTheme === "dark"
    ) {

        applyDarkMode(
            true,
            false
        );

    }


    const topButton =
        document.getElementById(
            "themeToggle"
        );


    if (topButton) {

        topButton.addEventListener(
            "click",
            () => {

                applyDarkMode(
                    !document.body.classList.contains(
                        "dark"
                    )
                );

            }
        );

    }


    const settingsButton =
        document.getElementById(
            "settingsThemeToggle"
        );


    if (settingsButton) {

        settingsButton.addEventListener(
            "click",
            () => {

                applyDarkMode(
                    !document.body.classList.contains(
                        "dark"
                    )
                );

            }
        );

    }


    updateThemeUI();

}


function applyDarkMode(
    enabled,
    notify = true
) {

    document.body.classList.toggle(
        "dark",
        enabled
    );


    localStorage.setItem(
        "realEstateTheme",
        enabled
            ? "dark"
            : "light"
    );


    updateThemeUI();


    if (mapInstance) {

        setTimeout(
            () => {

                mapInstance.invalidateSize();

            },
            150
        );

    }


    if (notify) {

        showToast(
            enabled
                ? "Dark mode enabled."
                : "Light mode enabled."
        );

    }

}


function updateThemeUI() {

    const dark =
        document.body.classList.contains(
            "dark"
        );


    const topButton =
        document.getElementById(
            "themeToggle"
        );


    if (topButton) {

        topButton.innerHTML =
            `
            <i data-lucide="${
                dark
                    ? "sun"
                    : "moon"
            }"></i>
            `;

    }


    const label =
        document.getElementById(
            "themeModeLabel"
        );


    if (label) {

        label.textContent =
            dark
                ? "Dark"
                : "Light";

    }


    const settingsButton =
        document.getElementById(
            "settingsThemeToggle"
        );


    if (settingsButton) {

        settingsButton.classList.toggle(
            "on",
            dark
        );

    }


    refreshIcons();

}


/* =========================================================
   NOTIFICATIONS
========================================================= */

function initializeNotifications() {

    const button =
        document.getElementById(
            "notificationBtn"
        );


    if (!button) {
        return;
    }


    button.addEventListener(
        "click",
        () => {

            showToast(
                "You have 3 new real estate insights."
            );

        }
    );

}


/* =========================================================
   HTML SECURITY
========================================================= */

function escapeHTML(value) {

    const element =
        document.createElement(
            "div"
        );


    element.textContent =
        String(
            value ?? ""
        );


    return element.innerHTML;

}