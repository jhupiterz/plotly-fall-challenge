if (!window.dash_clientside) {
    window.dash_clientside = {};
}
window.dash_clientside.clientside = {
    make_draggable: function(id1,id2) {
        setTimeout(function() {
            var el1 = document.getElementById(id1)
            var el2 = document.getElementById(id2)
            window.console.log(el1)
            window.console.log(el2)
            dragula([el1,el2])
        }, 1)
        return window.dash_clientside.no_update
    }
}