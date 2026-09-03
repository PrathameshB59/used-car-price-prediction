const projectTree =
    document.getElementById("projectTree");

const dumpTree =
    document.getElementById("dumpTree");

const activityLog =
    document.getElementById("activityLog");

const fileContent =
    document.getElementById("fileContent");

const selectedFile =
    document.getElementById("selectedFile");

const searchInput =
    document.getElementById("searchInput");

let projectItems = [];


// ============================================================
// HELPERS
// ============================================================

function formatSize(bytes) {

    if (!bytes || bytes <= 0) {
        return "0 B";
    }

    if (bytes < 1024) {
        return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
        return `${(
            bytes / 1024
        ).toFixed(1)} KB`;
    }

    if (bytes < 1024 * 1024 * 1024) {
        return `${(
            bytes /
            (1024 * 1024)
        ).toFixed(1)} MB`;
    }

    return `${(
        bytes /
        (1024 * 1024 * 1024)
    ).toFixed(2)} GB`;
}


function escapeText(value) {

    if (value === null ||
        value === undefined) {

        return "";
    }

    return String(value);
}


// ============================================================
// FILE TREE
// ============================================================

function renderItems(
    container,
    items
) {

    container.innerHTML = "";

    if (!items.length) {

        container.textContent =
            "No matching files.";

        return;
    }


    items.forEach((item) => {

        const row =
            document.createElement(
                "div"
            );

        row.className =
            "file-item";


        const name =
            document.createElement(
                "span"
            );

        name.className =
            "file-name";


        if (
            item.type ===
            "directory"
        ) {

            name.classList.add(
                "directory"
            );

            name.textContent =
                "📁 " +
                escapeText(
                    item.name
                );

        } else {

            name.textContent =
                "📄 " +
                escapeText(
                    item.name
                );
        }


        const metadata =
            document.createElement(
                "span"
            );

        metadata.className =
            "file-path";


        if (
            item.type ===
            "file"
        ) {

            metadata.textContent =
                `${item.path} · ${formatSize(
                    item.size
                )}`;

        } else {

            metadata.textContent =
                item.path;
        }


        row.appendChild(
            name
        );

        row.appendChild(
            metadata
        );


        if (
            item.type ===
            "file"
        ) {

            row.addEventListener(
                "click",
                () =>
                    openFile(
                        item.path
                    )
            );
        }


        container.appendChild(
            row
        );

    });
}


// ============================================================
// PROJECT
// ============================================================

async function loadProject() {

    try {

        const response =
            await fetch(
                "/dump/api/project/"
            );


        if (!response.ok) {

            throw new Error(
                "Project API failed."
            );
        }


        const data =
            await response.json();


        projectItems =
            data.items || [];


        renderItems(
            projectTree,
            projectItems
        );


    } catch (error) {

        projectTree.textContent =
            error.message;
    }
}


// ============================================================
// DUMP
// ============================================================

async function loadDump() {

    try {

        const response =
            await fetch(
                "/dump/api/activity/"
            );


        if (!response.ok) {

            throw new Error(
                "Dump API failed."
            );
        }


        const data =
            await response.json();


        activityLog.textContent =
            data.log || "";


        renderItems(
            dumpTree,
            data.items || []
        );


    } catch (error) {

        dumpTree.textContent =
            error.message;
    }
}


// ============================================================
// STATISTICS
// ============================================================

async function loadStats() {

    try {

        const response =
            await fetch(
                "/dump/api/stats/"
            );


        if (!response.ok) {

            throw new Error(
                "Statistics API failed."
            );
        }


        const data =
            await response.json();


        document.getElementById(
            "statFiles"
        ).textContent =
            data.files;


        document.getElementById(
            "statFolders"
        ).textContent =
            data.folders;


        document.getElementById(
            "statSize"
        ).textContent =
            formatSize(
                data.total_size
            );


    } catch (error) {

        document.getElementById(
            "statFiles"
        ).textContent =
            "-";

        document.getElementById(
            "statFolders"
        ).textContent =
            "-";

        document.getElementById(
            "statSize"
        ).textContent =
            "Unavailable";
    }
}


// ============================================================
// GIT
// ============================================================

async function loadGit() {

    try {

        const response =
            await fetch(
                "/dump/api/git/"
            );


        if (!response.ok) {

            throw new Error(
                "Git API failed."
            );
        }


        const data =
            await response.json();


        // Top cards

        document.getElementById(
            "branch"
        ).textContent =
            data.branch || "unknown";


        document.getElementById(
            "commit"
        ).textContent =
            data.commit || "unknown";


        document.getElementById(
            "tag"
        ).textContent =
            data.latest_tag || "none";


        // Git panel

        document.getElementById(
            "gitBranch"
        ).textContent =
            data.branch || "unknown";


        document.getElementById(
            "gitCommit"
        ).textContent =
            data.commit || "unknown";


        document.getElementById(
            "gitTag"
        ).textContent =
            data.latest_tag || "none";


        document.getElementById(
            "gitWorkingTree"
        ).textContent =
            data.clean
                ? "🟢 Clean"
                : "🟡 Changes";


        document.getElementById(
            "gitRemote"
        ).textContent =
            data.remote_url || "none";


        let syncText =
            "Unknown";


        if (
            data.ahead === 0 &&
            data.behind === 0
        ) {

            syncText =
                "🟢 In sync";

        } else {

            const parts = [];


            if (data.ahead > 0) {

                parts.push(
                    `${data.ahead} ahead`
                );
            }


            if (data.behind > 0) {

                parts.push(
                    `${data.behind} behind`
                );
            }


            syncText =
                "🟡 " +
                parts.join(
                    " · "
                );
        }


        document.getElementById(
            "gitSync"
        ).textContent =
            syncText;


        const lfs =
            data.lfs || {};


        document.getElementById(
            "gitLfs"
        ).textContent =
            lfs.available
                ? `🟢 ${lfs.count} tracked`
                : "Not available";


    } catch (error) {

        document.getElementById(
            "branch"
        ).textContent =
            "unknown";


        document.getElementById(
            "commit"
        ).textContent =
            "unknown";


        document.getElementById(
            "tag"
        ).textContent =
            "unknown";


        document.getElementById(
            "gitWorkingTree"
        ).textContent =
            error.message;
    }
}


// ============================================================
// GITHUB
// ============================================================

async function loadGithub() {

    try {

        const response =
            await fetch(
                "/dump/api/github/"
            );


        if (!response.ok) {

            throw new Error(
                "GitHub API failed."
            );
        }


        const data =
            await response.json();


        const online =
            document.getElementById(
                "githubOnline"
            );


        if (data.available) {

            online.textContent =
                "🟢 Online";


            document.getElementById(
                "githubRepo"
            ).textContent =
                data.full_name ||
                "Unknown";


            document.getElementById(
                "githubBranch"
            ).textContent =
                data.default_branch ||
                "Unknown";


            document.getElementById(
                "githubVisibility"
            ).textContent =
                data.private
                    ? "Private"
                    : "Public";


            document.getElementById(
                "githubStars"
            ).textContent =
                data.stars ?? 0;


            document.getElementById(
                "githubForks"
            ).textContent =
                data.forks ?? 0;


            document.getElementById(
                "githubIssues"
            ).textContent =
                data.open_issues ?? 0;


            const link =
                document.getElementById(
                    "githubLink"
                );


            link.href =
                data.html_url || "#";


            link.hidden =
                !data.html_url;


        } else {

            online.textContent =
                "🔴 Offline";


            document.getElementById(
                "githubRepo"
            ).textContent =
                data.full_name ||
                "Unavailable";


            document.getElementById(
                "githubBranch"
            ).textContent =
                "Local Git available";


            document.getElementById(
                "githubVisibility"
            ).textContent =
                "-";

        }


    } catch (error) {

        document.getElementById(
            "githubOnline"
        ).textContent =
            "🔴 Unavailable";
    }
}


// ============================================================
// HEALTH + DOCUMENTATION
// ============================================================

async function loadHealth() {

    const healthList =
        document.getElementById(
            "healthList"
        );


    const documentationList =
        document.getElementById(
            "documentationList"
        );


    try {

        const response =
            await fetch(
                "/dump/api/health/"
            );


        if (!response.ok) {

            throw new Error(
                "Health API failed."
            );
        }


        const data =
            await response.json();


        const health =
            data.health;


        document.getElementById(
            "healthPercentage"
        ).textContent =
            `${health.percentage}%`;


        healthList.innerHTML =
            "";


        health.checks.forEach(
            (check) => {

                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "health-item";


                const name =
                    document.createElement(
                        "span"
                    );

                name.className =
                    "health-name";

                name.textContent =
                    check.name;


                const status =
                    document.createElement(
                        "span"
                    );

                status.className =
                    check.ok
                        ? "health-ok"
                        : "health-fail";


                status.textContent =
                    check.ok
                        ? "✓ OK"
                        : "✕ Missing";


                row.appendChild(
                    name
                );

                row.appendChild(
                    status
                );

                healthList.appendChild(
                    row
                );
            }
        );


        documentationList.innerHTML =
            "";


        data.documentation.forEach(
            (doc) => {

                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "health-item";


                const name =
                    document.createElement(
                        "span"
                    );

                name.className =
                    "health-name";

                name.textContent =
                    doc.name;


                const status =
                    document.createElement(
                        "span"
                    );

                status.className =
                    doc.exists
                        ? "health-ok"
                        : "health-fail";


                status.textContent =
                    doc.exists
                        ? "✓ Present"
                        : "✕ Missing";


                row.appendChild(
                    name
                );

                row.appendChild(
                    status
                );


                documentationList.appendChild(
                    row
                );
            }
        );


    } catch (error) {

        healthList.textContent =
            error.message;

        documentationList.textContent =
            error.message;
    }
}


// ============================================================
// FILE VIEWER
// ============================================================

async function openFile(path) {

    selectedFile.textContent =
        path;


    fileContent.textContent =
        "Loading file...";


    try {

        const response =
            await fetch(
                `/dump/api/file/?path=${encodeURIComponent(
                    path
                )}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to open file."
            );
        }


        fileContent.textContent =
            data.content;


    } catch (error) {

        fileContent.textContent =
            error.message;
    }
}


// ============================================================
// SEARCH
// ============================================================

function searchProject() {

    const query =
        searchInput.value
            .toLowerCase()
            .trim();


    if (!query) {

        renderItems(
            projectTree,
            projectItems
        );

        return;
    }


    const filtered =
        projectItems.filter(
            (item) =>
                item.name
                    .toLowerCase()
                    .includes(query)
                ||
                item.path
                    .toLowerCase()
                    .includes(query)
        );


    renderItems(
        projectTree,
        filtered
    );
}


// ============================================================
// RELEASES
// ============================================================

async function loadReleases() {

    const releaseList =
        document.getElementById(
            "releaseList"
        );


    try {

        const response =
            await fetch(
                "/dump/api/releases/"
            );


        if (!response.ok) {

            throw new Error(
                "Release API failed."
            );
        }


        const data =
            await response.json();


        const releases =
            data.releases || [];


        releaseList.innerHTML =
            "";


        if (!releases.length) {

            releaseList.textContent =
                "No Git tags found.";

            return;
        }


        releases.forEach(
            (release) => {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "release-item";


                const header =
                    document.createElement(
                        "div"
                    );

                header.className =
                    "release-header";


                const tag =
                    document.createElement(
                        "span"
                    );

                tag.className =
                    "release-tag";

                tag.textContent =
                    release.tag;


                const commit =
                    document.createElement(
                        "span"
                    );

                commit.className =
                    "release-commit";

                commit.textContent =
                    release.commit;


                header.appendChild(
                    tag
                );

                header.appendChild(
                    commit
                );


                const subject =
                    document.createElement(
                        "div"
                    );

                subject.className =
                    "release-subject";

                subject.textContent =
                    release.subject ||
                    "No commit message";


                const date =
                    document.createElement(
                        "div"
                    );

                date.className =
                    "release-date";

                date.textContent =
                    release.date ||
                    "";


                item.appendChild(
                    header
                );

                item.appendChild(
                    subject
                );

                item.appendChild(
                    date
                );


                releaseList.appendChild(
                    item
                );
            }
        );


    } catch (error) {

        releaseList.textContent =
            error.message;
    }
}


// ============================================================
// REFRESH EVENTS
// ============================================================

document
    .getElementById(
        "refreshProject"
    )
    .addEventListener(
        "click",
        loadProject
    );


document
    .getElementById(
        "refreshDump"
    )
    .addEventListener(
        "click",
        loadDump
    );


document
    .getElementById(
        "refreshGit"
    )
    .addEventListener(
        "click",
        loadGit
    );


document
    .getElementById(
        "refreshGithub"
    )
    .addEventListener(
        "click",
        loadGithub
    );


document
    .getElementById(
        "refreshReleases"
    )
    .addEventListener(
        "click",
        loadReleases
    );


searchInput.addEventListener(
    "input",
    searchProject
);


// ============================================================
// INITIAL LOAD
// ============================================================

loadProject();

loadDump();

loadStats();

loadGit();

loadGithub();

loadHealth();

loadReleases();
