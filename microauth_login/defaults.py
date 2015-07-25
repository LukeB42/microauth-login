# Default configuration settings for microauth-login

config = {
    "server":               "https://localhost:7789/v1/",
    "apikey":               "",
    "use_remote_settings":  0,     # switch to true to attempt to use a config served by the server
    "permit_root_logon":    0,     # don't handle authenticating as the superuser
    "create_accounts":      1,     # create accounts for successful users?
    "defer_to_original":    1,     # should we use the original program if the server is unavailable?
    "limit":                "5,30m", # retry limit
    "allow_groups":         "",
    "deny_groups":          "nologin",
    "priority":             "deny",
}
