
var j$ = jQuery;
var sgsCmdHandler = new SgsCmdHandler();

var updater = {
    errorSleepTime: 500,

    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        $.ajax({
            url: "/sgs/cmd",
            type: "GET",
            dataType: "json",
            data: $.param(args),
            success: updater.onSuccess,
            error: updater.onError
        });
    },

    onSuccess: function(response) {
        try {
            updater.handleCmd(response.cmds);
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    handleCmd: function(cmds) {
        for (var i = 0; i < cmds.length; i++) {
            sgsCmdHandler.handle(cmds[i]);
        }
    }
};

var initButtonsEvent = function() {
    j$(".btn.ready").click(function() {
        var cmd = genCmd("READY");
        sendCmd(cmd);
    });
    j$(".btn.unready").click(function() {
        var cmd = genCmd("UNREADY");
        sendCmd(cmd);
    });
}

var sendJoinCmd = function() {
    var cmd = genCmd("JOIN");
    sendCmd(cmd);
}

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    initButtonsEvent();
    sendJoinCmd();
});

