const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

const resultSection =
    document.getElementById("resultSection");

const result =
    document.getElementById("result");

const loading =
    document.getElementById("loading");

const errorMessage =
    document.getElementById("errorMessage");

const copyButton =
    document.getElementById("copyButton");

const statusDot =
    document.getElementById("statusDot");

const statusText =
    document.getElementById("statusText");


/* -------------------------
   TAB SWITCHING
-------------------------- */

tabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        const target =
            tab.dataset.tab;

        tabs.forEach((item) => {
            item.classList.remove("active");
        });

        tab.classList.add("active");

        tabContents.forEach((content) => {
            content.classList.remove("active");
        });

        document
            .getElementById(target)
            .classList.add("active");

        hideResult();
    });

});


/* -------------------------
   UI HELPERS
-------------------------- */

function showLoading(button) {

    resultSection.classList.remove("hidden");

    errorMessage.classList.add("hidden");

    result.textContent = "";

    loading.classList.remove("hidden");

    if (button) {
        button.disabled = true;
    }
}


function hideLoading(button) {

    loading.classList.add("hidden");

    if (button) {
        button.disabled = false;
    }
}


function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");
}


function hideResult() {

    resultSection.classList.add("hidden");

    loading.classList.add("hidden");

    errorMessage.classList.add("hidden");

    result.textContent = "";
}


function displayResult(text) {

    resultSection.classList.remove("hidden");

    result.textContent = text;

    result.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}


/* -------------------------
   API REQUEST
-------------------------- */

async function sendRequest(
    url,
    body,
    button
) {

    showLoading(button);

    try {

        const response =
            await fetch(url, {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(body)

            });


        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error(
                "The server returned an invalid response."
            );
        }


        if (!response.ok) {

            let message =
                data.detail ||
                "Something went wrong.";

            if (Array.isArray(message)) {

                message = message
                    .map((item) =>
                        item.msg || "Invalid input."
                    )
                    .join(", ");

            }

            throw new Error(message);
        }


        displayResult(
            data.result || "No response received."
        );

    } catch (error) {

        showError(
            error.message ||
            "Unable to connect to EduGenie."
        );

    } finally {

        hideLoading(button);

    }
}


/* -------------------------
   ASK
-------------------------- */

const askButton =
    document.getElementById("askButton");


askButton.addEventListener(
    "click",
    async () => {

        const question =
            document
                .getElementById("question")
                .value
                .trim();

        const level =
            document
                .getElementById("askLevel")
                .value;


        if (!question) {

            showError(
                "Please enter a question."
            );

            resultSection.classList.remove(
                "hidden"
            );

            return;
        }


        await sendRequest(
            "/api/ask",
            {
                question,
                level
            },
            askButton
        );

    }
);


/* -------------------------
   SUMMARIZE
-------------------------- */

const summarizeButton =
    document.getElementById(
        "summarizeButton"
    );


summarizeButton.addEventListener(
    "click",
    async () => {

        const text =
            document
                .getElementById(
                    "summaryText"
                )
                .value
                .trim();


        if (!text) {

            resultSection.classList.remove(
                "hidden"
            );

            showError(
                "Please enter text to summarize."
            );

            return;
        }


        await sendRequest(
            "/api/summarize",
            {
                text
            },
            summarizeButton
        );

    }
);


/* -------------------------
   QUIZ
-------------------------- */

const quizButton =
    document.getElementById(
        "quizButton"
    );


quizButton.addEventListener(
    "click",
    async () => {

        const topic =
            document
                .getElementById(
                    "quizTopic"
                )
                .value
                .trim();

        const count =
            Number(
                document
                    .getElementById(
                        "quizCount"
                    )
                    .value
            );

        const difficulty =
            document
                .getElementById(
                    "quizDifficulty"
                )
                .value;

        const level =
            document
                .getElementById(
                    "quizLevel"
                )
                .value;


        if (!topic) {

            resultSection.classList.remove(
                "hidden"
            );

            showError(
                "Please enter a quiz topic."
            );

            return;
        }


        await sendRequest(
            "/api/quiz",
            {
                topic,
                count,
                difficulty,
                level
            },
            quizButton
        );

    }
);


/* -------------------------
   LEARNING PATH
-------------------------- */

const learningButton =
    document.getElementById(
        "learningButton"
    );


learningButton.addEventListener(
    "click",
    async () => {

        const goal =
            document
                .getElementById(
                    "learningGoal"
                )
                .value
                .trim();

        const level =
            document
                .getElementById(
                    "learningLevel"
                )
                .value;

        const weeks =
            Number(
                document
                    .getElementById(
                        "learningWeeks"
                    )
                    .value
            );


        if (!goal) {

            resultSection.classList.remove(
                "hidden"
            );

            showError(
                "Please enter your learning goal."
            );

            return;
        }


        await sendRequest(
            "/api/learning-path",
            {
                goal,
                level,
                weeks
            },
            learningButton
        );

    }
);


/* -------------------------
   COPY
-------------------------- */

copyButton.addEventListener(
    "click",
    async () => {

        const text =
            result.textContent.trim();


        if (!text) {
            return;
        }


        try {

            await navigator.clipboard.writeText(
                text
            );

            const original =
                copyButton.textContent;

            copyButton.textContent =
                "✓ Copied";

            setTimeout(() => {

                copyButton.textContent =
                    original;

            }, 1500);

        } catch {

            showError(
                "Could not copy the response."
            );

        }

    }
);


/* -------------------------
   HEALTH CHECK
-------------------------- */

async function checkHealth() {

    try {

        const response =
            await fetch(
                "/api/health"
            );


        if (!response.ok) {
            throw new Error();
        }


        const data =
            await response.json();


        if (data.status === "ok") {

            statusDot.classList.add(
                "online"
            );

            statusText.textContent =
                "EduGenie online";

        }

    } catch {

        statusText.textContent =
            "Server unavailable";

    }

}


checkHealth();