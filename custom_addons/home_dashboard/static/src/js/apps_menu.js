/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";
import { fuzzyLookup } from "@web/core/utils/search";

export class HomeAppsMenu extends Component {
    static template = "home_dashboard.AppsMenu";

    setup() {
        this.state = useState({
            isOpen: false,
            searchTerm: "",
        });
        this.searchInput = useRef("searchInput");
    }

    get apps() {
        return this.props.apps || [];
    }

    get filteredApps() {
        if (!this.state.searchTerm) {
            return this.apps;
        }
        return fuzzyLookup(this.state.searchTerm, this.apps, (app) => app.name) || [];
    }

    toggle() {
        this.state.isOpen = !this.state.isOpen;
        if (this.state.isOpen) {
            setTimeout(() => {
                if (this.searchInput.el) {
                    this.searchInput.el.focus();
                }
            }, 100);
        }
    }

    close() {
        this.state.isOpen = false;
        this.state.searchTerm = "";
    }

    onSearchInput(ev) {
        this.state.searchTerm = ev.target.value;
    }

    onAppClick(app) {
        this.props.onNavBarDropdownItemSelection(app);
        this.close();
    }

    getAppIcon(app) {
        if (app.webIconData) {
            return `data:image/png;base64,${app.webIconData}`;
        }
        if (app.webIcon) {
            return `/${app.webIcon}`;
        }
        return "/web/static/img/odoo-icon.svg";
    }
}

// Register HomeAppsMenu component to NavBar
NavBar.components = { ...NavBar.components, HomeAppsMenu };
