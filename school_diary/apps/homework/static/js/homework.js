import {API} from '/static/js/inbuiltAPI.js';


String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}


const homeworkApp = new Vue({
    el: "#homework-app",
    delimiters: ["[[", "]]"],
    data: {
        homework: undefined,
        date: ["week"]
    },
    methods: {
        getHomework: function(start=null, end=null) {
            let vm = this;
            this.homework = undefined;
            if (start && !end) {
                this.date = ["day", start];
                end = start;
            } else if (!(start || end)) {
                this.date = ["week"];
                let now = new Date();
                let range_end = new Date();
                range_end.setDate(now.getDate() + 7);
                end = range_end.toISOString().split("T")[0];
                start = now.toISOString().split("T")[0];
            }
            else if (start && end) {
                this.date = ["range", start, end];
            }
            API.homework.list((data) => {
                vm.homework = data;
                vm.$nextTick(function() {
                    document.querySelectorAll("code").forEach(value => {
                        const code = value.innerHTML;
                        value.innerHTML = `<div class="show-code">Показать код</div>`
                        value.addEventListener('click', function (e) {
                            let modal = new bootstrap.Modal(document.getElementById("code-snippet-modal"), {})
                            document.getElementById("code-snippet-modal-code").innerHTML = code;
                            modal.show();
                        })
                    })
                    let clipboard = new ClipboardJS('#code-snippet-modal-code');
                    clipboard.on('success', function (e) {
                        e.clearSelection();
                        let tooltip =  new bootstrap.Tooltip(document.getElementById('code-snippet-modal-code'), {
                            title: "Скопировано!",
                            delay: { "show": 500, "hide": 100 },
                            placement: 'bottom'
                        });
                        tooltip.show();
                    });
                    clipboard.on('error', function(e) {
                        console.log(e);
                    })
                })
            }, [["date_before", end], ["date_after", start]]);
        },
        getDate: function(date) {
            if (date[0] === "week") return "Домашнее задание на неделю";
            let d1 = new Date(date[1]);
            d1 = d1.toLocaleDateString("ru", {
                weekday: "short", day: "numeric", month: "long"
            }).capitalize();
            if (date[1] !== "range") return d1;
            let d2 = new Date(date[2]);
            d2 = d2.toLocaleDateString("ru", {
                weekday: "short", day: "numeric", month: "long"
            }).capitalize();
            return "От " + d1 + " до " + d2;
        },
        getDateBadge: function(date) {
            let d = new Date(date);
            return d.toLocaleDateString("ru", {
                weekday: "short"
            }).capitalize();
        },
        showOrDownload: function(e) {
            let href = e.target.href;
            function performExtensionCheck(href) {
                for (let value of ['.jpg', '.png', '.jpeg']) {
                    if (href.endsWith(value)) return true;
                }
                return false;
            }
            if (performExtensionCheck(href)) {
                e.preventDefault();
                let image = new Image();
                image.src = href;
                let v = new Viewer(image, {
                    navbar: false,
                    toolbar: {
                        play: {show: false},
                        zoomIn: {show: true},
                        zoomOut: {show: true},
                        oneToOne: {show: true},
                        reset: {show: true},
                        prev: {show: false},
                        next: {show: false},
                        rotateLeft: {show: true},
                        rotateRight: {show: true},
                        flipHorizontal: {show: true},
                        flipVertical: {show: true},
                    }
                });
                v.show();
            }
        },
    }
})


document.getElementById("dateSelectBtn").addEventListener("click", ev => {
    let date = document.getElementById("id_date").value;
    homeworkApp.getHomework(date);
})


document.getElementById("weekHwBtn").addEventListener("click", ev => {
    ev.preventDefault();
    homeworkApp.getHomework();
})

document.addEventListener("DOMContentLoaded", function(event) {
  homeworkApp.getHomework();
});

