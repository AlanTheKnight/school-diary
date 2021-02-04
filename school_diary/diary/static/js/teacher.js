const csrf = Cookies.get("csrftoken");

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
      $.ajax({
        headers: {
          "X-CSRFToken": csrf,
        },
        data: {
          date: date,
          theme: theme,
          control: control,
        },
        url: "/api/inbuilt/lessons/edit-lesson/" + pk,
        method: "PATCH",
        success: function (data) {
          refreshSelection();
        },
      });
    },
  },
});

const modalApp = new Vue({
  el: "#delete-lesson",
  delimiters: ["[[", "]]"],
  data: {
    id: undefined,
  },
});

const planApp = new Vue({
  el: "#plan-lesson",
  delimiters: ["[[", "]]"],
  data: {
    id: undefined,
  },
});

function refresh(group, quarter) {
  $.ajax({
    url: "/api/inbuilt/lessons/list-lessons",
    method: "GET",
    data: {
      group: group,
      term: quarter,
    },
    success: function (data) {
      app.lessons = data;
      grades_app.refreshTable(group, quarter);
    },
  });
}

function showMenu(that) {
  modalApp.id = $(that).parent().attr("id");
  $("#delete-lesson").modal("toggle");
}

function getControls() {
  $.ajax({
    url: "/api/inbuilt/list-controls",
    method: "GET",
    success: function (data) {
      app.controls = data;
    },
  });
}

getControls();
refreshSelection();

function changeLessonPlanState(id) {
  $.ajax({
    url: "/api/inbuilt/lessons/change-is-plan",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrf,
      lesson: Number(id),
    },
    success: function (data) {
      refreshSelection();
      $("#plan-lesson").modal("hide");
    },
  });
}

function deleteLesson(id) {
  $.ajax({
    url: "/api/inbuilt/lessons/delete-lesson/" + id,
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrf,
    },
    data: {
      lesson: Number(id),
    },
    success: function (data) {
      refreshSelection();
      $("#delete-lesson").modal("hide");
    },
  });
}

function changePlanState(that) {
  planApp.id = $(that).parent().attr("id");
  $("#plan-lesson").modal("toggle");
}

function renderAvg(s) {
  if (s === null) return "-";
  return Number(s).toPrecision(2).replace(".", ",");
}

function saveMark(that) {
  $(that).parent().addClass("grade-changed");

  $.each($(that).attr("class").split(/\s+/), function (index, item) {
    if (item.startsWith("grade-")) {
      $(that).removeClass(item);
    }
  });
  $(that).addClass("grade-" + $(that).val());

  let value = Number(that.value); // Value of mark
  let mark_data = that.name.split("|").map((x) => Number(x));
  $.ajax({
    url: "/api/inbuilt/save-mark",
    method: "POST",
    headers: {
      "X-CSRFToken": csrf,
    },
    data: {
      student: mark_data[0],
      lesson: mark_data[1],
      value: value,
    },
    success: function (data) {
      let sm_avg = $("#s_" + mark_data[0]);
      let avg = $("#" + mark_data[0]);
      sm_avg.html(renderAvg(data.sm_avg));
      avg.html(renderAvg(data.avg));
    },
  });
}

function commentDialog(that) {
  let data = that.name.split("|").map((x) => Number(x));
  let csrf = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url: "/api/inbuilt/get-comment",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrf,
      lesson: data[1],
      student: data[0],
    },
    success: function (data) {
      if (data.status === "aborted") return;
      $("#comment-text").val(data.comment);
      $("#comment-hidden").val(that.name);
      $("#comment-modal").modal("show");
    },
  });
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
    refreshTable: function (group, quarter) {
      $.ajax({
        headers: {
          "X-CSRFToken": csrf,
        },
        data: {
          group: group,
          quarter: quarter,
        },
        method: "POST",
        url: "/api/inbuilt/lessons/grades",
        success: function (data) {
          grades_app.grades = data;
          if (data.lessons !== undefined && data.lessons.length !== 0) {
            grades_app.header = grades_app.getLessonMonths();
          }
        },
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
        if (d == new Date(lessons[i].date).getMonthName()) {
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
  },
});

String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

Date.prototype.getMonthName = function () {
  return this.toLocaleString("ru", { month: "long" }).capitalize();
};

function getDateDay(date) {
  return new Date(date).getDate();
}

function refreshSelection() {
  let subject = $("#id_subjects").val();
  let klass = $("#id_classes").val();
  let quarter = Number($("#id_quarters").val());
  $.ajax({
    headers: {
      "X-CSRFToken": csrf,
    },
    url: "/api/inbuilt/lessons/get-group",
    method: "POST",
    data: {
      klass_id: Number(klass),
      subject_id: Number(subject),
    },
    success: function (data) {
      if (data) {
        grades_app.refreshTable(data.id, quarter);
        refresh(data.id, quarter);
        Cookies.set("group_id", data.id);
        Cookies.set("quarter", quarter);
      }
    },
  });
}
//
const editLesson = new Vue({
  el: "#editLessonApp",
  delimiters: ["[[", "]]"],
  data: {
    lesson: undefined,
  },
});

function editLessonModal(event, lesson) {
  $.ajax({
    url: "/api/inbuilt/lessons/" + String(lesson.id),
    method: "GET",
    success: function (data) {
      editLesson.lesson = data;
      const prefix = "edit";
      const fields = ["homework", "theme", "date", "is_planned", "control", "id"]
      for (let field of fields) {
          $("#id_" + prefix + "-" + field).val(data[field]);
      }
      $("#editLessonModal").modal("show");
    }
  })
}