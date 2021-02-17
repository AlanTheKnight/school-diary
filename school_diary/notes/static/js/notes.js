"use strict"

function getFileSize(bytes) {
    let amounts = ["", "КБ", "МБ", "ГБ"];
    let counter = 0;
    while (bytes > 1024 && counter < 3) {
        bytes = Math.round((bytes / 1024 + Number.EPSILON) * 100) / 100;
        counter++;
    }
    return String(bytes) + amounts[counter]
}


const app1 = new Vue({
    el: "#feed",
    delimiters: ["[[", "]]"],
    data: {
        notes: undefined
    },
    methods: {
        getNotesList: function () {
            $.ajax({
                url: '/notes/api/notes/',
                method: "GET",
                success: function (data) {
                    app1.notes = data;
                }
            });
        },
        getDate: (date) => {
            return new Date(date).toLocaleDateString("ru", {month: "long", day: "numeric"})
        },
    }
})

const app2 = new Vue({
    el: "#my-notes-list",
    delimiters: ["[[", "]]"],
    data: {
        notes: undefined
    },
    methods: {
        getNotesList: function () {
            $.ajax({
                url: '/notes/api/my-notes',
                method: "GET",
                success: function (data) {
                    app2.notes = data;
                }
            });
        },
        initGroupEdit: function (pk) {
            notesGroupEditApp.notesGroupId = pk;
            $("#create-and-view-list").hide();
            notesGroupEditApp.refreshGroup(true);
        },
    }
})

app1.getNotesList();
app2.getNotesList();


const notesGroupEditApp = new Vue({
    el: "#notes-group-edit",
    delimiters: ["[[", "]]"],
    data: {
        notesGroupId: undefined,
        notesGroup: undefined,
        notes: undefined,
        droppedFiles: undefined,
    },
    methods: {
        refreshGroup: function (initForm = false) {
            let vm = this;
            $.ajax({
                url: '/notes/api/notes/' + vm.notesGroupId,
                method: "GET",
                success: function (data) {
                    vm.notes = data.notes;
                    vm.notesGroup = data;
                    if (initForm) {
                        vm.initDragNDropBox();
                    }
                }
            })
        },
        goToMainPage: function () {
            this.notes = undefined;
            this.notesGroup = undefined;
            $("#create-and-view-list").show();
        },
        initDragNDropBox: function () {
            let vm = this;
            this.$nextTick(() => {
                let form = $("#dragFileForm");
                let box = $("#dragFileBox");
                box.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                })
                .on("dragover dragenter", function (event) {
                    box.addClass("is-dragover");
                })
                .on("dragend dragleave drop", function (event) {
                    box.removeClass("is-dragover");
                })
                .on("drop", function (event) {
                    vm.droppedFiles = event.originalEvent.dataTransfer.files;
                    form.submit();
                })

                $("#file").on("change", (e) => {
                    form.submit();
                })

                form.on("submit", function (e) {
                    e.preventDefault();
                    // if (!(vm.droppedFiles.length > 0 || ))
                    let ajaxData = new FormData(form[0]);
                    $.each(vm.droppedFiles, (i, file) => {
                        ajaxData.append("files", file);
                    })
                    vm.droppedFiles = undefined;
                    ajaxData.append("group", notesGroupEditApp.notesGroupId);
                    $.ajax({
                        url: "/notes/api/upload-notes",
                        method: "post",
                        data: ajaxData,
                        dataType: 'json',
                        cache: false,
                        contentType: false,
                        processData: false,
                        complete: function () {
                            vm.refreshGroup();
                            app2.getNotesList();
                            app1.getNotesList();
                        },
                    });
                })
            });
        },
        deleteNote: function (pk, event) {
            const csrf = Cookies.get("csrftoken");
            $.ajax({
                url: '/notes/api/delete-note/' + pk,
                method: 'delete',
                headers: {
                    "X-CSRFToken": csrf,
                },
                success: function (data) {
                    notesGroupEditApp.refreshGroup();
                }
            })
            $(event.target).css("display", "none");
        },
        showImage: function (event) {
            let vm = this;
            new Viewer(this.$refs.photos, {
                ready () {
                    this.viewer.show();
                },
                hidden() {
                    this.viewer.destroy();
                }
            });
        },
        showImageMenu: function (event) {
            event.preventDefault();
            let photoDiv = $(event.target).parent();
            photoDiv.find('.delete-note').css("display", "block");
            return false;
        }
    },
})

