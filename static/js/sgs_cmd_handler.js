
var j$ = jQuery;
var MAX_SEAT = 0;

var SgsCmdHandler = function() {

    var self = this;

    self._is_me = function(cmd) {
        return cmd.sender == UID;
    };

    self._ack_join = function() {
        updater.poll();
    };

    self._ack_ready = function() {
        j$(".btn.ready").hide();
        j$(".btn.unready").show();
    };

    self._ack_unready = function() {
        j$(".btn.unready").hide();
        j$(".btn.ready").show();
    };

    self._game_msg = function(cmd) {
        $(".game-table .info-panel").html(
                cmd.msg + "<br />"
                + $(".game-table .info-panel").html());
    };

    self._game_start = function() {
        j$(".btn.ready").hide();
        j$(".btn.unready").hide();
        j$(".btn.logout").hide();
    };

    self._join = function(cmd) {
        if(self._is_me(cmd)) {
            j$(".player-0").attr("id", "seat-" + cmd.seat_id);
            MAX_SEAT = cmd.max_seat;
            for(i = 1; i < MAX_SEAT; i ++) {
                j$(".player-" + i).attr(
                        "id", "seat-" + ((cmd.seat_id + i) % MAX_SEAT));
            }
        } else {
            j$("#seat-" + cmd.seat_id).html(j$("#player-tpl").html());
            j$("#seat-" + cmd.seat_id + " .name").html(cmd.sender);
        }
    };

    self._ready = function(cmd) {
        if(self._is_me(cmd)) {
            j$(".btn.ready").hide();
            j$(".btn.unready").show();
        } else {
            j$("#seat-" + cmd.seat_id).addClass("player-ready");
        }
    };

    self._set_figure = function(cmd) {
        j$(".self .figure").html(cmd.figure_name);
        j$(".figure-candidate-popup").modal("hide");
    };

    self._set_figure_candidate = function(cmd) {
        for(i in cmd.figures) {
            var figure = j$("#figure-candidate-tpl").clone();
            figure.attr("data-pk", cmd.figures[i].pk);
            figure.find(".name").html(cmd.figures[i].name);
            figure.removeClass("hide")
                  .removeAttr("id");
            figure.find("a").click(function() {
                genAndSendCmd(
                    "CHOOSE_FIGURE",
                    {figure_id:
                        j$(this).parents(".figure-candidate").data("pk")
                    });
            });
            j$(".figure-candidate-popup .figures").prepend(figure);
        }
        j$(".figure-candidate-popup").modal("show");
    };

    self._set_role = function(cmd) {
        j$(".self .role").html(cmd.label);
    };

    self._show_figure = function(cmd) {
        for(i in cmd.figures) {
            j$("#seat-" + cmd.seat_id + " .figure").html(
                    cmd.figures[i].name);
        }
    };

    self._show_role = function(cmd) {
        j$("#seat-" + cmd.seat_id + " .role").html(cmd.label);
    }

    self._unready = function(cmd) {
        if(self._is_me(cmd)) {
        } else {
            j$("#seat-" + cmd.seat_id).removeClass("player-ready");
        }
    };

    self.cmd_mapping = {
        // A-Z
        "ACK_JOIN": self._ack_join,
        "ACK_READY": self._ack_ready,
        "ACK_UNREADY": self._ack_unready,
        "GAME_MSG": self._game_msg,
        "GAME_START": self._game_start,
        "JOIN": self._join,
        "READY": self._ready,
        "SET_FIGURE": self._set_figure,
        "SET_FIGURE_CANDIDATE": self._set_figure_candidate,
        "SET_ROLE": self._set_role,
        "SHOW_FIGURE": self._show_figure,
        "SHOW_ROLE": self._show_role,
        "UNREADY": self._unready
    };

    self.handle = function(cmd) {
        console.log(cmd);
        $(".game-table .info-panel").html(
                cmd.cmd + "<br />"
                + $(".game-table .info-panel").html());
        if(cmd.cmd in self.cmd_mapping) {
            self.cmd_mapping[cmd.cmd](cmd);
        }
    };

};
