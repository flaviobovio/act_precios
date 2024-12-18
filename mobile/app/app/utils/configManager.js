// App configuration

import * as ApplicationSettings from "@nativescript/core/application-settings";

export default {
  saveConfig(config) {
    ApplicationSettings.setString("backend", config.backend || "http://127.0.0.1:5000/");
    ApplicationSettings.setString("token", config.token || "");
  },

  loadConfig() {
    const backend = ApplicationSettings.getString("backend", "Not set");
    const token = ApplicationSettings.getString("token", "");
    return { backend, token };
  },
};
