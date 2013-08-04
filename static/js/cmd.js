
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

var sendCmd = function(cmd) {
    $.postJSON("/sgs/cmd", cmd, function(response) {
        updater.handleCmd(response.cmds);
    });
}

var genCmdFromStr = function(str) {
    var tmp = str.split(" ");
    var cmd = {cmd: tmp[0]};
    tmp = tmp[1].split(",");
    for(i in tmp) {
        var kwarg = tmp[i].split("=");
        cmd[kwarg[0]] = kwarg[1];
    }
    return cmd;
};

var genCmd = function(cmd, args) {
    var rtn = {
        cmd: cmd,
    };
    for(k in args) {
        rtn[k] = args[k];
    }
    return rtn;
};

var genAndSendCmd = function(cmd, args) {
    sendCmd(genCmd(cmd, args));
};
