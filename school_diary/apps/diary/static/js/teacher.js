import {API} from './inbuiltAPI.js';

const app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        lessons: undefined,
        controls: undefined,
    },
    methods: {
        editLessonInfo: function (pk) {
            let date = $("#date" + pk).val();
            let theme = $("#theme" + pk).val();
            let control = Number($("#control" + pk).val());
            let data = {
                date: date,
                theme: theme,
                control: control,
            };
            API.lessons.edit(pk, data);
        },
        refresh: function () {
            let d = {
                group: Cookies.get("group_id"),
                quarter: Cookies.get("quarter"),
            };
            API.lessons.list(d, function (data) {
                app.lessons = data;
            })
        },
        changePlanned: function (pk, is_planned) {
            planApp.pk = pk;
            planApp.previousState = is_planned;
            $("#plan-lesson").modal("toggle");
        },
        showMenu: function (pk) {
            modalApp.pk = pk;
            $("#delete-lesson").modal("toggle");
        },
    },
    mounted: function () {
        let vm = this;
        API.controls.list(function (data) {
            vm.controls = data;
        })
    }
});

const modalApp = new Vue({
    el: "#delete-lesson",
    delimiters: ["[[", "]]"],
    data: {
        pk: undefined,
    },
    methods: {
        deleteLesson: function (e) {
            if (!this.pk) return;
            API.lessons.delete(this.pk, function (data) {
                $("#delete-lesson").modal("hide");
                app.refresh();
            });
        },
    }
});

const planApp = new Vue({
    el: "#plan-lesson",
    delimiters: ["[[", "]]"],
    data: {
        pk: undefined,
        previousState: undefined,
    },
    methods: {
        changePlanned: function () {
            let d = {
                is_planned: !this.previousState
            }
            API.lessons.edit(this.pk, d, function () {
                app.refresh();
            })
            $("#plan-lesson").modal("hide");
        }
    }
});

function commentDialog(that) {
    let data = that.name.split("|").map((x) => Number(x));
    let csrf = $("input[name='csrfmiddlewaretoken']").val();
    API.comments.get(data[0], data[1], function (data) {
        if (data.status === "aborted") return;
        $("#comment-text").val(data.comment);
        $("#comment-hidden").val(that.name);
        $("#comment-modal").modal("show");
    })
}

function addComment() {
    let commentText = $("#comment-text").val();
    let data = $("#comment-hidden")
        .val()
        .split("|")
        .map((x) => Number(x));
    let csrf = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: "/api/inbuilt/add-comment",
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrf,
            comment: commentText,
            lesson: data[1],
            student: data[0],
        },
    });
    $("#comment-text").val("");
    $("#comment-modal").modal("hide");
}

const grades_app = new Vue({
    el: "#grades-app",
    delimiters: ["[[", "]]"],
    data: {
        grades: undefined,
        header: undefined,
    },
    methods: {
        refreshTable: function () {
            let v = this;
            API.getGradesTable(Cookies.get("group_id"), Cookies.get("quarter"), function (data) {
                v.grades = data;
                if (data.lessons !== undefined && data.lessons.length !== 0) {
                    v.header = grades_app.getLessonMonths();
                }
            });
        },
        showPopover: function (e, lesson) {
            e.preventDefault();
            $(e.target).popover({
                html: true,
                content: `${lesson.control_name}<br><b>Тема урока: </b>${lesson.theme}`,
                title: this.getLessonDateTitle(lesson.date),
            });
            $(e.target).popover("toggle");
        },
        getLessonDateTitle: function (date) {
            let d = new Date(date);
            return d
                .toLocaleString("ru", {
                    weekday: "long",
                    month: "long",
                    day: "numeric",
                })
                .capitalize();
        },
        getLessonMonths: function () {
            const lessons = this.grades.lessons;
            let data = [];
            let count = 1;
            for (let i = 1; i < lessons.length; i++) {
                let d = new Date(lessons[i - 1].date).getMonthName();
                if (d === new Date(lessons[i].date).getMonthName()) {
                    count++;
                } else {
                    data.push([d, count]);
                    count = 1;
                }
            }
            data.push([
                new Date(lessons[lessons.length - 1].date).getMonthName(),
                count,
            ]);
            return data;
        },
        getGrade: function (student, lesson) {
            for (let i = 0; i < student.grades.length; i++) {
                if (student.grades[i].lesson_id === lesson.id) {
                    return student.grades[i];
                }
            }
            return undefined;
        },
        getAllGrades: function (student, lessons) {
            return lessons.map(function (lesson) {
                return grades_app.getGrade(student, lesson);
            });
        },
        getDateDay: function (date) {
            return new Date(date).getDate();
        },
        renderAvg: function (s) {
            if (s === null) return "-";
            return Number(s).toPrecision(2).replace(".", ",");
        },
        editLessonModal: function (event, lesson) {
            API.lessons.get(lesson.id, data => {
                const modal = new bootstrap.Modal(document.getElementById("editLessonModal"));
                const prefix = "edit";
                const fields = ["homework", "theme", "date", "is_planned", "control", "id"]
                for (let field of fields) {
                    let fieldInput = $("#id_" + prefix + "-" + field)
                    fieldInput.val(data[field]);
                    fieldInput.attr("name", field);
                }
                modal.show();
                let form = document.querySelector("#editLessonModal form");
                form.onsubmit = function (e) {
                    e.preventDefault();
                    let fd = new FormData(form);
                    API.lessons.edit(
                        lesson.id, fd,
                        (data) => {
                            modal.hide();
                            grades_app.refreshTable();
                        },
                        {
                            processData: false,
                            contentType: false,
                            dataType: 'json',
                            enctype: 'multipart/form-data',
                        });
                }
            })
        },
        saveGrade: function (student, lesson, event) {
            const value = event.target.value;
            let v = this;
            API.grades.save(
                {
                    student: student,
                    lesson: lesson,
                    value: value
                }, (data) => {
                    document.getElementById("avg" + student).innerHTML = this.renderAvg(data.avg);
                    document.getElementById("sm_avg" + student).innerHTML = this.renderAvg(data.sm_avg);
                    const cell = document.getElementById('cell-' + student + '-' + lesson);
                    /**
                     * @type {Array}
                     */
                    let scope = v.grades.scope;
                    let r = scope.find(value1 => value1.student.pk === student);
                    console.log(r);
                    if (!cell.classList.contains('grade-changed')) cell.classList.add('grade-changed');
                }
            )
        }
    },
});

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

Date.prototype.getMonthName = function () {
    return this.toLocaleString("ru", {month: "long"}).capitalize();
};


function refreshSelection() {
    let subject = $("#id_subjects").val();
    let klass = $("#id_classes").val();
    let quarter = Number($("#id_quarters").val());
    let data = {
        klass_id: Number(klass),
        subject_id: Number(subject),
    };
    API.groups.get(data, function (data) {
        Cookies.set("group_id", data.id);
        Cookies.set("quarter", quarter);
        grades_app.refreshTable();
    });
}


refreshSelection();


document.getElementById("grades-tab").addEventListener('shown.bs.tab', function (event) {
    grades_app.refreshTable();
})

document.getElementById("lessons-tab").addEventListener('shown.bs.tab', function (event) {
    app.refresh();
})
