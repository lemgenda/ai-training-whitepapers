document.addEventListener("DOMContentLoaded", () => {
    const tabsNav = document.querySelector(".tabs-nav");
    if (!tabsNav) return;

    // Move tabs-nav to be a direct child of .container, placed right after the header
    const container = document.querySelector(".container");
    const header = document.querySelector("header");
    if (container && header) {
        container.insertBefore(tabsNav, header.nextSibling);
    }

    // Create a sentinel element to place just before the tabs-nav
    const sentinel = document.createElement("div");
    sentinel.className = "tabs-nav-sentinel";
    sentinel.style.position = "absolute";
    sentinel.style.height = "1px";
    sentinel.style.width = "1px";
    sentinel.style.pointerEvents = "none";
    sentinel.style.visibility = "hidden";
    
    // Insert the sentinel right before tabsNav
    tabsNav.parentNode.insertBefore(sentinel, tabsNav);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const rect = entry.boundingClientRect;
            // Sentinel has scrolled above the top of the viewport
            if (!entry.isIntersecting && rect.top < 0) {
                tabsNav.classList.add("stuck");
            } else {
                tabsNav.classList.remove("stuck");
            }
        });
    }, {
        threshold: [0]
    });

    observer.observe(sentinel);
});
