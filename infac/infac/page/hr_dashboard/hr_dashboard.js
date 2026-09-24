// frappe.pages['hr-dashboard'].on_page_load = function(wrapper) {

//     const page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'HR Dashboard',
//         single_column: true
//     });

//     frappe.breadcrumbs.add('infac');

//     /* ==============================
//        CORE CENTER LAYOUT (YOUR NEED)
//     ===============================*/
//     const style = document.createElement('style');
//     style.innerHTML = `

//         /* ⭐ CENTER LIKE HUMAN RESOURCE DASHBOARD */
//         .page-content-wrapper {
//             display: flex;
//             justify-content: center;
//         }

        
//         .dashboard-wrapper {
//             width: 80%;
//             max-width: 1400px;
//             margin: 0 auto;
//             padding: 20px;
//             background: #f5f7fb;
//         }

//         /* 📱 responsive */
//         @media (max-width: 1400px) {
//             .dashboard-wrapper { width: 75%; }
//         }
//         @media (max-width: 1100px) {
//             .dashboard-wrapper { width: 90%; }
//         }
//         @media (max-width: 768px) {
//             .dashboard-wrapper {
//                 width: 100%;
//                 padding: 12px;
//             }
//         }

//         .page-header {
//             text-align: center;
//             margin-bottom: 20px;
//         }

//         .filter-bar {
//             display: flex;
//             justify-content: center;
//             gap: 10px;
//             flex-wrap: wrap;
//             margin-top: 12px;
//         }

//         .hr-layout {
//             display: flex;
//             flex-direction: column;
//             gap: 20px;
//         }

//         .hr-card {
//             background: #fff;
//             border-radius: 14px;
//             box-shadow: 0 4px 14px rgba(0,0,0,0.06);
//             padding: 16px;
//             border: 1px solid #e5e7eb;
//             width: 100%;
//         }

//         .hr-card h3 {
//             font-size: 15px;
//             font-weight: 600;
//             margin-bottom: 12px;
//         }

//         .hr-table {
//             width: 100%;
//             border-collapse: collapse;
//             font-size: 13px;
//         }

//         .hr-table thead th {
//             background: #f3f4f6;
//             padding: 8px;
//             border-bottom: 1px solid #e5e7eb;
//             text-align: center;
//             font-weight: 600;
//         }

//         .hr-table td {
//             padding: 8px;
//             border-bottom: 1px solid #f1f5f9;
//         }

//         .hr-table td:first-child,
//         .hr-table th:first-child {
//             text-align: left;
//         }

//         .hr-table tbody tr:hover {
//             background: #f9fafb;
//         }

//         .leave-circle, .late-circle {
//             width: 150px;
//             height: 150px;
//             border-radius: 50%;
//             margin: 15px auto;
//             position: relative;
//         }
//         .dept-card {
//             background: #fff;
//             border-radius: 12px;
//             padding: 14px;
//             cursor: pointer;
//             transition: all 0.2s ease;
//             border: 1px solid #e5e7eb;
//         }

//         .dept-card:hover {
//             transform: translateY(-4px);
//             box-shadow: 0 8px 20px rgba(0,0,0,0.08);
//         }

//         .dept-card-header {
//             font-weight: 600;
//             font-size: 15px;
//             margin-bottom: 10px;
//         }

//         .stat-row {
//             display: flex;
//             justify-content: space-between;
//             font-size: 13px;
//             padding: 2px 0;
//         }
//             .click-plan,
//         .click-present {
//             cursor: pointer;
//             font-weight: 600;
//         }

//         .click-plan:hover,
//         .click-present:hover {
//             text-decoration: underline;
//         }

//         .dept-cards-grid {
//             display: grid;
//             grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
//             gap: 14px;
//         }

//         .dept-card {
//             background: #fff;
//             border-radius: 12px;
//             padding: 14px;
//             box-shadow: 0 2px 8px rgba(0,0,0,.08);
//             transition: .2s ease;
//         }

//         .dept-card:hover {
//             transform: translateY(-3px);
//         }

//         .dept-title {
//             font-weight: 600;
//             margin-bottom: 10px;
//         }

//         .dept-stat {
//             display: flex;
//             justify-content: space-between;
//             margin: 6px 0;
//             padding: 6px 10px;
//             border-radius: 6px;
//             cursor: pointer;
//         }

//         .stat-available { background: #eef4ff; }
//         .stat-present   { background: #e9f9ee; }
//         .stat-absent    { background: #ffecec; }

//         .dept-stat:hover {
//             opacity: 0.85;
//         }

//         .dashboard-cards {
//             display: flex;
//             gap: 20px;
//             margin-top: 25px;
//             flex-wrap: wrap;
//         }

//         .custom-card {
//             flex: 1;
//             min-width: 220px;
//             padding: 20px;
//             border-radius: 14px;
//             color: #fff;
//             cursor: pointer;
//             transition: 0.3s ease;
//             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
//         }

//         .custom-card h4 {
//             margin: 0;
//             font-size: 15px;
//             font-weight: 500;
//             opacity: 0.9;
//         }

//         .custom-card h2 {
//             margin-top: 10px;
//             font-size: 28px;
//             font-weight: 600;
//         }
//             .hr-row {
//             display: flex;
//             justify-content: space-between;
//             gap: 20px;
//             margin-top: 20px;
//         }

//         .hr-card {
//             flex: 1;
//             padding: 20px;
//             border-radius: 12px;
//             background: white;
//             box-shadow: 0 4px 10px rgba(0,0,0,0.08);
//         }

//         .center {
//             text-align: center;
//         }
//             .late-card{
//             cursor:pointer;
//             text-align:center;
//         }

//         .custom-card:hover {
//             transform: translateY(-6px);
//             box-shadow: 0 8px 20px rgba(0,0,0,0.25);
//         }

//         .center { text-align: center; }
//         .muted { color: #64748b; }
//     `;
//     document.head.appendChild(style);

//     /* ==============================
//        HTML (UNCHANGED — YOUR TABLES)
//     ===============================*/
//     $(wrapper).html(`
//         <div class="dashboard-wrapper">

//             <div class="page-header">
//                 <h2>HR Dashboard</h2>

//                 <div class="filter-bar">
//                     <input type="date" id="filter-date" class="form-control" style="width:200px;">
//                     <select id="shift" class="form-control" style="width:200px;">
//                         <option value="All">All Shift</option>
//                         <option value="A">A</option>
//                         <option value="B">B</option>
//                         <option value="C">C</option>
//                         <option value="G">G</option>
//                     </select>
//                     <button id="apply-filter" class="btn btn-primary">Apply</button>
//                 </div>
//             </div>

//             <div class="hr-layout">

//                 <!-- Head Count -->
//                 <div class="hr-card">
//                     <h3>Head Count Details</h3>
//                     <div class="table-responsive">
//                         <table class="hr-table">
//                             <thead>
//                                 <tr>
//                                     <th rowspan="2">Department</th>
//                                     <th colspan="4">Overall</th>
//                                     <th colspan="3">1st Shift</th>
//                                     <th colspan="3">General Shift</th>
//                                     <th colspan="3">2nd Shift</th>
//                                     <th colspan="3">3rd Shift</th>
//                                 </tr>
//                                 <tr>
//                                     <th>Avail</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>
//                                     <th>%</th>
//                                     <th>Plan</th><th>Present</th><th>Absent</th>
//                                     <th>Plan</th><th>Present</th><th>Absent</th>
//                                     <th>Plan</th><th>Present</th><th>Absent</th>
//                                     <th>Plan</th><th>Present</th><th>Absent</th>
//                                 </tr>
//                             </thead>
//                             <tbody id="dept-summary-body"></tbody>
//                         </table>
//                     </div>
//                 </div>


// <!-- Department Quick Cards -->
// <div class="hr-card mt-4">
//     <h3>Department Quick View</h3>
//     <div id="dept-cards-container" class="dept-cards-grid"></div>
// </div>

//                 <div class="row">

//     <!-- LEFT SIDE : Weekly Table -->
//         <div class="col-md-6">
//             <div class="hr-card">
//                 <h3>Weekly Attendance Summary Graph</h3>

//                 <div class="filter-bar" style="display:flex;gap:10px;margin-bottom:10px;">
//                     <input type="date" id="from-date" class="form-control" style="width:180px;">
//                     <input type="date" id="to-date" class="form-control" style="width:180px;">
//                     <button id="apply-weekly-filter" class="btn btn-primary">Apply</button>
//                 </div>

//                 <canvas id="weeklyAttendanceChart" height="120"></canvas>
//             </div>
//         </div>

//     <!-- RIGHT SIDE : Weekly Graph -->
//         <div class="col-md-6">
//             <div class="hr-card">
//                 <h3>Weekly Attendance Summary Table</h3>
//                 <div class="table-responsive">
//                     <table class="hr-table">
//                         <thead>
//                             <tr>
//                                 <th>Date</th>
//                                 <th>Plan</th>
//                                 <th>Actual</th>
//                                 <th>Gap</th>
//                                 <th>%</th>
//                             </tr>
//                         </thead>
//                         <tbody id="weekly-attendance-body"></tbody>
//                     </table>
//                 </div>
//             </div>
//      </div>   
// </div>

//                 <!-- Contractor -->
//                 <div class="hr-card">
//                     <h3>Contractor Wise Attendance</h3>
//                     <div class="table-responsive">
//                         <table class="hr-table">
//                             <thead>
//                                 <tr>
//                                     <th>Contractor Name</th>
//                                     <th>Available</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>
//                                 </tr>
//                             </thead>
//                             <tbody id="late-reason-body">
//                                 <tr><td colspan="4" class="center">Loading...</td></tr>
//                             </tbody>
//                         </table>
//                     </div>
//                 </div>

                
// <div class="row">
//     <!-- LEFT SIDE : SUMMARY TABLE -->
//     <div class="col-md-9">

//         <div class="hr-card" style="width:100%;">

//             <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">

//                 <h3 style="margin:0;">Late Entry Details</h3>

//                 <div style="display:flex;gap:8px;">
//                     <input type="date" id="late-from-date" class="form-control" style="width:150px;">
//                     <input type="date" id="late-to-date" class="form-control" style="width:150px;">

//                     <button class="btn btn-primary btn-sm" id="late-filter-btn">
//                         Apply
//                     </button>
//                 </div>
//             </div>

//             <div class="table-responsive">
//                 <table class="hr-table" id="late-summary-table">
//                     <thead>
//                         <tr>
//                             <th>Shift/Category</th>
//                             <th>Staff</th>
//                             <th>Worker</th>
//                             <th>NAPS</th>
//                             <th>Contract</th>
//                             <th>Trainee</th>
//                         </tr>
//                     </thead>

//                     <tbody id="late-summary-body">
//                         <tr>
//                             <td colspan="6" style="text-align:center;padding:16px;">
//                                 Loading...
//                             </td>
//                         </tr>
//                     </tbody>
//                 </table>
//            </div>
//         </div>
//     </div>

//     <!-- RIGHT SIDE : CARD -->
//     <div class="col-md-3">
//         <div class="hr-card late-card" id="late-card">
//           <h4>Total Late Employees</h4>
//             <h1 id="late-count">0</h1>
//         </div>
//     </div>
// </div>


// <!--PERMISSION TABLE -->

// <div class="row">
//     <div class="col-md-9">
//         <div class="hr-card" id="permission-summary-card">
//     <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
//         <h3 style="margin:0;">Permission Summary</h3>
//         <div style="display:flex; gap:8px;">
//             <input type="date" id="perm-from-date" class="form-control" style="width:150px;">
//             <input type="date" id="perm-to-date" class="form-control" style="width:150px;">
//             <button class="btn btn-primary btn-sm" id="perm-filter-btn">Apply</button>
//         </div>
//     </div>

//     <table class="table table-bordered">
//         <thead>
//             <tr style="background-color:#e9ecef; color:#333; font-weight:600;">
//                 <th>Shift/Category</th>
//                 <th>Staff</th>
//                 <th>Worker</th>
//                 <th>NAPS</th>
//                 <th>Contract</th>
//                 <th>Trainee</th>
//             </tr>
//         </thead>
//         <tbody id="perm-summary-body"></tbody>
//     </table>
// </div>
//     </div>

//     <div class="col-md-3">
//         <div class="hr-card late-card"
//              id="perm-count-card"
//              style="cursor:pointer; text-align:center;">
//             <h4>Total Permission Employees</h4>
//             <h1 id="perm-count">0</h1>
//         </div>
//     </div>
// </div>

//         <!-- Leave Sumamry Table -->

//                  <div class="hr-card" id="leave-summary-card">
//                     <h3>Leave Summary</h3>

//                     <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">

//                         <div style="display:flex; gap:10px; align-items:center;">
//                             <input type="date" id="leave-from-date" class="form-control" style="width:180px;">
//                             <input type="date" id="leave-to-date" class="form-control" style="width:180px;">
//                             <button class="btn btn-primary btn-sm" id="leave-filter-btn">Apply</button>
//                             <button class="btn btn-success btn-sm" id="leave-download-btn">Download </button>
//                         </div>

//                         <div id="leave-count-box" style="margin-right:50px;"></div>

//                     </div>

//                     <div id="leave-detail-table"></div>
//                 </div>
                            
//                 <!-- Dept Line -->

//                <div class="hr-card">
//     <div class="d-flex justify-content-between align-items-center mb-2">
//         <h3 class="mb-0">Department Line Summary</h3>

//         <button class="btn btn-sm btn-success" onclick="downloadDeptLineSummary()">
//             Download
//         </button>
//     </div>

//     <div class="table-responsive">
//         <table id="dept_line_summary" class="hr-table">
//             <thead>
//                 <tr>
//                     <th>Department Line</th>
//                     <th>Available</th>
//                     <th>Present</th>
//                     <th>Absent</th>
//                     <th>Absent %</th>
//                 </tr>
//             </thead>
//             <tbody></tbody>
//         </table>
//     </div>
// </div>

//             </div>
//         </div>
//     `);

//     // ✅ default date
//     const $date = $(wrapper).find('#filter-date');
//     $date.val(frappe.datetime.get_today());



// // ✅ default today for permission filter
// const today_perm = frappe.datetime.get_today();
// $(wrapper).find("#perm-from-date").val(today_perm);
// $(wrapper).find("#perm-to-date").val(today_perm);

// // ✅ auto load
// setTimeout(() => {
//     load_permission_summary();
// }, 300);

// $(wrapper).on("click", "#perm-filter-btn", function () {
//     load_permission_summary();
// });

// function load_permission_summary() {

//     let from_date = $(wrapper).find("#perm-from-date").val();
//     let to_date   = $(wrapper).find("#perm-to-date").val();

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_permission_summary",
//         args: {
//             from_date: from_date,
//             to_date: to_date
//         },
//         callback: function (r) {

//     let data = r.message.summary || [];
//     let total = r.message.total || 0;

//     let html = "";

//     data.forEach(row => {

//         html += `
//             <tr>
//                 <td>${row.shift || ""}</td>
//                 <td>${row.staff || 0}</td>
//                 <td>${row.worker || 0}</td>
//                 <td>${row.naps || 0}</td>
//                 <td>${row.contract || 0}</td>
//                 <td>${row.trainee || 0}</td>
//             </tr>
//         `;
//     });

//     $("#perm-summary-body").html(html);

//     $("#perm-count").text(total);
// }
//     });
// }

// function show_permission_employees() {

//     const from_date = $(wrapper).find("#perm-from-date").val();
//     const to_date = $(wrapper).find("#perm-to-date").val();

//     if (!from_date || !to_date) {
//         frappe.msgprint("Please select From and To Date");
//         return;
//     }

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_permission_employees",
//         args: {
//             from_date: from_date,
//             to_date: to_date
//         },
//         callback: function (r) {

//             let data = r.message || [];

//             let html = `
//                     <div style="text-align:right; margin-bottom:10px;">
//                         <button class="btn btn-success btn-sm" id="perm-download-btn">
//                             Download Excel
//                         </button>
//                     </div>
//                     <table class="table table-bordered table-sm">
//                         <thead>
//                             <tr>
//                                 <th>Employee ID</th>
//                                 <th>Name</th>
//                                 <th>Shift</th>
//                                 <th>Session</th>
//                                 <th>From Time</th>
//                                 <th>To Time</th>
//                                 <th>Status</th>
//                                 <th>Approver</th> 
//                                 <th>Created On</th>
//                             </tr>
//                         </thead>
//                         <tbody>
//                 `;

//                 if (data.length === 0) {
//                    html += `<tr><td colspan="9" style="text-align:center;">No records found</td></tr>`;
//                 } else {
//                     data.forEach(emp => {
//                         // format created_on to readable date DD-MM-YYYY
//                         let created = "";
//                             if (emp.created_on) {
//                                 let date_part = emp.created_on.split(" ")[0];
//                                 let time_part = emp.created_on.split(" ")[1].split(".")[0];

//                                 let parts = date_part.split("-");
//                                 let day   = parts[2].padStart(2, "0");
//                                 let month = parts[1].padStart(2, "0");
//                                 let year  = parts[0];

//                                 created = `${day}-${month}-${year} ${time_part}`;
//                             }

//                         // color badge for status
//                         let status_color = "secondary";
//                         if (emp.status === "Approved") status_color = "success";
//                         else if (emp.status === "Rejected") status_color = "danger";
//                         else if (emp.status === "Pending") status_color = "warning";

//                         html += `
//                             <tr>
//                                 <td>${emp.employee_id || ""}</td>
//                                 <td>${emp.employee_name || ""}</td>
//                                 <td>${emp.shift || ""}</td>
//                                 <td>${emp.session || ""}</td>
//                                 <td>${emp.from_time || ""}</td>
//                                 <td>${emp.to_time || ""}</td>
//                                 <td>
//                                     <span class="badge badge-${status_color}">
//                                         ${emp.status || ""}
//                                     </span>
//                                 </td>
//                                 <td>${emp.approver || ""}</td> 
//                                 <td>${created}</td>
//                             </tr>
//                         `;
//                     });
//                 }

//                 html += `</tbody></table>`;
//             let d = new frappe.ui.Dialog({
//                 title: `Permission Employees`,
//                 size: "extra-large",
//                 fields: [{ fieldtype: "HTML", fieldname: "table_html" }]
//             });

//             d.fields_dict.table_html.$wrapper.html(html);

//             // Bind click AFTER html is rendered into dialog
//             d.fields_dict.table_html.$wrapper.find("#perm-download-btn").on("click", function () {
//                 window.open(
//                     `/api/method/infac.infac.page.hr_dashboard.hr_dashboard.download_permission_excel?from_date=${from_date}&to_date=${to_date}`
//                 );
//             });
            
//             d.show();
//         }
//     });
// }

// function download_permission_excel() {
//     const from_date = $(wrapper).find("#perm-from-date").val();
//     const to_date   = $(wrapper).find("#perm-to-date").val();
//     window.open(
//         `/api/method/infac.infac.page.hr_dashboard.hr_dashboard.download_permission_excel?from_date=${from_date}&to_date=${to_date}`
//     );
// }

// // function render_permission_table(data) {
// //     if (!data.length) {
// //         $("#perm-detail-table").html(
// //             `<p style="color:red;">No Permission Records Found</p>`
// //         );
// //         return;
// //     }

// //     let html = `
// //         <table class="table table-bordered table-sm">
// //             <thead>
// //                 <tr>
// //                     <th>Employee ID</th>
// //                     <th>Employee Name</th>
// //                     <th>Session</th>
// //                     <th>From Time</th>
// //                     <th>To Time</th>
// //                 </tr>
// //             </thead>
// //             <tbody>
// //     `;

// //     data.forEach(row => {
// //         html += `
// //             <tr>
// //                 <td>${row.employee_id || ""}</td>
// //                 <td>${row.employee_name || ""}</td>
// //                 <td>${row.session || ""}</td>
// //                 <td>${row.from_time || ""}</td>
// //                 <td>${row.to_time || ""}</td>
// //             </tr>
// //         `;
// //     });

// //     html += `</tbody></table>`;

// //     $("#perm-detail-table").html(html);
// // }

// //  auto load
// setTimeout(() => {
//     load_leave_app_summary();
// }, 300);

// $(wrapper).on("click", "#leave-filter-btn", function () {
//     load_leave_app_summary();
// });

// const today_leave = frappe.datetime.get_today();
// $(wrapper).find("#leave-from-date").val(today_leave);
// $(wrapper).find("#leave-to-date").val(today_leave);

// function load_leave_app_summary() {
//     let from_date = $("#leave-from-date").val();
//     let to_date = $("#leave-to-date").val();

//     if (!from_date || !to_date) {
//         frappe.msgprint("Please select From and To Date");
//         return;
//     }

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_leave_app_summary",
//         args: {
//             from_date: from_date,
//             to_date: to_date
//         },
//         callback: function (r) {
//             let data = r.message.details || [];

//             render_leave_app_table(data);
//             $("#leave-count-box").html(`
//                 <div style="
//                     background:#fff;
//                     border:1px solid #d1d8dd;
//                     border-radius:6px;
//                     padding:8px 15px;
//                     text-align:center;
//                     min-width:180px;
//                 ">
//                     <div style="font-size:18px;font-weight:bold;color:#000;">Total Leave</div>
//                     <div style="font-size:22px;font-weight:bold;color:#000;">
//                         ${data.length}
//                     </div>
//                 </div>
//             `);
//         }
//     });
// }
// function render_leave_app_table(data) {
//     if (!data.length) {
//         $("#leave-detail-table").html(
//             `<p style="color:red;">No Leave Records Found</p>`
//         );
//         return;
//     }

//     let html = `
//         <table class="table table-bordered table-sm" style="table-layout:auto; width:100%;">
//             <thead>
//                 <tr>
//                     <th>Employee ID</th>
//                     <th>Employee Name</th>
//                     <th>From Date</th>
//                     <th>To Date</th>
//                     <th>Leave Type</th>
//                     <th style="width:300px;">Reason</th>
//                     <th>Status</th>
//                     <th>Approver</th>
//                 </tr>
//             </thead>
//             <tbody>
//     `;

//     data.forEach(row => {
//         html += `
//             <tr>
//                 <td style="white-space:nowrap;">${row.employee || ""}</td>
//                 <td style="white-space:nowrap;">${row.employee_name || ""}</td>
//                 <td style="white-space:nowrap;">${frappe.datetime.str_to_user(row.from_date || "")}</td>
//                 <td style="white-space:nowrap;">${frappe.datetime.str_to_user(row.to_date || "")}</td>
//                 <td style="white-space:nowrap;">${row.leave_type || ""}</td>

//                 <td style="
//                     max-width:300px;
//                     white-space:normal;
//                     word-break:break-word;
//                 ">
//                     ${row.description || ""}
//                 </td>

//                 <td style="white-space:nowrap;">${row.workflow_state || ""}</td>
//                 <td style="white-space:nowrap;">${row.approver || ""}</td>
//             </tr>
//         `;
//     });

//     html += `</tbody></table>`;

//     $("#leave-detail-table").html(html);
// }

// $(wrapper).on("click", "#leave-download-btn", function () {
//     download_leave_csv();
// });

// function download_leave_csv() {
//     let from_date = $("#leave-from-date").val();
//     let to_date = $("#leave-to-date").val();

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_leave_app_summary",
//         args: { from_date, to_date },
//         callback: function (r) {
//             let data = r.message.details || [];

//             if (!data.length) {
//                 frappe.msgprint("No data to download.");
//                 return;
//             }

//             // Define columns
//             let headers = ["Employee ID", "Employee Name", "Leave Type", "Session", "From Date", "To Date", "Half Day", "Total Leave Days","Status", "Approver"];
//             let rows = data.map(row => [
//                 row.employee || "",
//                 row.employee_name || "",
//                 row.leave_type || "",
//                 row.session || "",
//                 row.from_date || "",
//                 row.to_date || "",
//                 row.half_day || "",
//                 row.total_leave_days || "",
//                 row.workflow_state || "",
//                 row.approver || ""

//             ]);

//             // Build CSV string
//             let csv_content = [headers, ...rows]
//                 .map(row => row.map(val => `"${val}"`).join(","))
//                 .join("\n");

//             // Trigger download
//             let blob = new Blob([csv_content], { type: "text/csv;charset=utf-8;" });
//             let url = URL.createObjectURL(blob);
//             let a = document.createElement("a");
//             a.href = url;
//             a.download = `Leave_Summary_${from_date}_to_${to_date}.csv`;
//             a.click();
//             URL.revokeObjectURL(url);
//         }
//     });
// }

// const loadData = () => {
//     const attendance_date =
//         document.getElementById("filter-date")?.value ||
//         frappe.datetime.get_today();

//     const $tbody = $("#dept-summary-body");

//     // Loading state
//     $tbody.html(
//         `<tr><td colspan="20" class="muted text-center p-3">Loading...</td></tr>`
//     );

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_dept_summary",
//         args: { attendance_date },
//         callback: (r) => {
//             const data = r.message || [];

//             if (!data.length) {
//                 $tbody.html(
//                     `<tr><td colspan="20" class="text-center muted p-3">No data</td></tr>`
//                 );
//                 $("#dept-card-container").html(""); // clear cards
//                 return;
//             }

//             // ✅ TABLE RENDER
//             let rows = "";
//             data.forEach(d => {
//                 const absent_pct = (d.absent_pct ?? 0).toFixed(1) + "%";
//                 const bg = d.bg_color || "";

//                 rows += `
//                     <tr style="background:${bg}">
//                         <td>${frappe.utils.escape_html(d.department)}</td>
//                         <td class="text-center">
//     <span class="click-plan text-primary"
//           data-dept="${frappe.utils.escape_html(d.department)}"
//           data-date="${attendance_date}">
//         ${d.available}
//     </span>
// </td>

// <td class="text-center">
//     <span class="click-present text-success"
//           data-dept="${frappe.utils.escape_html(d.department)}"
//           data-date="${attendance_date}">
//         ${d.present}
//     </span>
// </td>
//                         <td class="text-center text-danger">${d.absent}</td>
//                         <td class="text-center"><b>${absent_pct}</b></td>
//                         ${renderShiftCols(d["1st Shift"])}
//                         ${renderShiftCols(d["General"])}
//                         ${renderShiftCols(d["2nd Shift"])}
//                         ${renderShiftCols(d["3rd Shift"])}
//                     </tr>
//                 `;
//             });

//             $tbody.html(rows);

//             // ✅ CARD RENDER (MOVED INSIDE)
//             const $cardContainer = $("#dept-card-container");
//             let cards = "";

//             data.forEach(d => {
//                 const absent_pct = (d.absent_pct ?? 0).toFixed(1);

//                 cards += `
//                     <div class="col-md-4 col-lg-3">
//                         <div class="dept-card shadow-sm"
//                              data-dept="${frappe.utils.escape_html(d.department)}"
//                              data-date="${attendance_date}">

//                             <div class="dept-card-header">
//                                 ${frappe.utils.escape_html(d.department)}
//                             </div>

//                             <div class="dept-card-body">
//                                 <div class="stat-row">
//                                     <span>Available</span>
//                                     <b class="text-primary">${d.available}</b>
//                                 </div>

//                                 <div class="stat-row">
//                                     <span>Present</span>
//                                     <b class="text-success">${d.present}</b>
//                                 </div>

//                                 <div class="stat-row">
//                                     <span>Absent</span>
//                                     <b class="text-danger">${d.absent}</b>
//                                 </div>

//                                 <div class="stat-row">
//                                     <span>Absent %</span>
//                                     <b>${absent_pct}%</b>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 `;
//             });

//             $cardContainer.html(cards);
//             renderDeptCards(data, attendance_date);
//         }
//     });
// };


// const renderDeptCards = (data, attendance_date) => {
//     const $wrap = $("#dept-cards-container");

//     if (!data.length) {
//         $wrap.html(`<div class="muted">No department data</div>`);
//         return;
//     }

//     let html = "";

//     data.forEach(d => {
//         html += `
//             <div class="dept-card">
//                 <div class="dept-title">${frappe.utils.escape_html(d.department)}</div>

//                 <div class="dept-stat stat-available click-plan"
//                      data-dept="${d.department}"
//                      data-date="${attendance_date}">
//                     <span>Available</span>
//                     <b>${d.available}</b>
//                 </div>

//                 <div class="dept-stat stat-present click-present"
//                      data-dept="${d.department}"
//                      data-date="${attendance_date}">
//                     <span>Present</span>
//                     <b>${d.present}</b>
//                 </div>

//                 <div class="dept-stat stat-absent">
//                     <span>Absent</span>
//                     <b>${d.absent}</b>
//                 </div>
//             </div>
//         `;
//     });

//     $wrap.html(html);
// };

// const today = frappe.datetime.get_today();

// $("#late-from-date").val(today);
// $("#late-to-date").val(today);

// setTimeout(() => {
//     loadLateSummary();
// }, 500);

// $(document).on("click","#late-card",function(){

//     show_late_employees();
// });

// $(document).on("click", "#late-filter-btn", function () {

//     loadLateSummary();

// });

// $(document).on("click","#download-late-btn",function(){
//     download_late_excel();
// });



// function renderShiftCols(shift) {
//     if (!shift) return `<td class="text-center">0</td><td class="text-center">0</td><td class="text-center">0</td>`;
//     return `
//         <td class="text-center text-primary">${shift.plan}</td>
//         <td class="text-center text-success">${shift.present}</td>
//         <td class="text-center text-danger">${shift.absent}</td>
//     `;
// }

// document.getElementById("filter-date")?.addEventListener("change", loadData);


// window.loadDeptLineSummary = function () {
//         const attendance_date = $date.val();
//         const shift = $("#shift").val() || "All";

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard.hr_dashboard.get_dept_line_summary",
//             args: { attendance_date, shift },
//             callback: function (r) {
//                 const data = r.message || [];
//                 const tbody = $("#dept_line_summary tbody");
//                 tbody.empty();

//                 if (!data.length) {
//                     tbody.append(`<tr><td colspan="5" class="text-center text-muted">No data</td></tr>`);
//                     return;
//                 }

//                 data.forEach(row => {
//                 let rowStyle = "";

//                 if (row.department_line && row.department_line.trim().toLowerCase() === "total") {
//                     // Highlight Total row
//                     rowStyle = `font-weight:bold; background-color:#e3f2fd;`; // light blue background + bold
//                 } else if (row.bg_color) {
//                     rowStyle = `background-color:${row.bg_color};`;
//                 }

//                 tbody.append(`
//                     <tr style="${rowStyle}">
//                         <td>${row.department_line}</td>
//                         <td class="text-center">${row.available}</td>
//                         <td class="text-center">${row.present}</td>
//                         <td class="text-center">${row.absent}</td>
//                         <td class="text-center">${row.absent_pct}%</td>
//                     </tr>
//                 `);
//             });

//             }
//         });
//     };

//     // --- DOWNLOAD FUNCTION ---
//     window.downloadDeptLineSummary = function () {
//         const table = document.getElementById("dept_line_summary");
//         if (!table) return frappe.msgprint("No table found to download.");
//         const wb = XLSX.utils.table_to_book(table, { sheet: "Dept Line Summary" });
//         XLSX.writeFile(wb, "Department_Line_Summary.xlsx");
//     };

//     // function loadLateSummary() {

//     //     const attendance_date =
//     //         document.getElementById("filter-date")?.value ||
//     //         frappe.datetime.get_today();

//     //     const tbody = document.getElementById("late-summary-body");

//     //     tbody.innerHTML = `
//     //         <tr>
//     //             <td colspan="6" style="text-align:center;padding:16px;">
//     //                 Loading...
//     //             </td>
//     //         </tr>
//     //     `;

//     //     frappe.call({
//     //         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_late_summary",
//     //         args: {
//     //             attendance_date: attendance_date
//     //         },
//     //         callback: function (r) {

//     //             const data = r.message || [];

//     //             if (!data.length) {
//     //                 tbody.innerHTML = `
//     //                     <tr>
//     //                         <td colspan="6" style="text-align:center;padding:16px;">
//     //                             No data
//     //                         </td>
//     //                     </tr>
//     //                 `;
//     //                 return;
//     //             }

//     //             let rows = "";

//     //             data.forEach(d => {

//     //                 let style = "";

//     //                 if (d.Description === "Total") {
//     //                     style = "font-weight:bold;background:#f3f4f6;";
//     //                 }

//     //                 rows += `
//     //                     <tr style="${style}">
//     //                         <td>${d.Description || "-"}</td>
//     //                         <td style="text-align:center">${d.STAFF || 0}</td>
//     //                         <td style="text-align:center">${d.WORKER || 0}</td>
//     //                         <td style="text-align:center">${d.NAPS || 0}</td>
//     //                         <td style="text-align:center">${d.Contract || 0}</td>
//     //                         <td style="text-align:center">${d.Trainee || 0}</td>
//     //                     </tr>
//     //                 `;
//     //             });

//     //             tbody.innerHTML = rows;

//     //         }
//     //     });

//     // }

//     function loadLateSummary() {

//     const from_date = $("#late-from-date").val();
//     const to_date = $("#late-to-date").val();

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard.hr_dashboard.get_late_summary",
//         args: {
//             from_date: from_date,
//             to_date: to_date
//         },
//         callback: function (r) {

//             let data = r.message.summary || [];
//             let total = r.message.total || 0;

//             let html = "";

//             data.forEach(row => {

//                 html += `
//                     <tr>
//                         <td>${row.description}</td>
//                         <td>${row.staff || 0}</td>
//                         <td>${row.worker || 0}</td>
//                         <td>${row.naps || 0}</td>
//                         <td>${row.contract || 0}</td>
//                         <td>${row.trainee || 0}</td>
//                     </tr>
//                 `;

//             });

//             $("#late-summary-body").html(html);

//             // ⭐ Update Card Count
//             $("#late-count").text(total);

//         }
//     });

// }
//     function load_late_count(){

//         frappe.call({
//             method:"infac.infac.page.hr_dashboard.hr_dashboard.get_late_count",
//             callback:function(r){

//                 document.getElementById("late-count").innerText = r.message;

//             }
//         })

// }

// function load_late_count(){

//         frappe.call({
//             method:"infac.infac.page.hr_dashboard.hr_dashboard.get_permission_count",
//             callback:function(r){

//                 document.getElementById("perm-count").innerText = r.message;

//             }
//         })

// }
// // Add this with your other click bindings
// $(wrapper).on("click", "#perm-count-card", function () {
//     show_permission_employees();
// });
//     // function show_late_employees(){

//     //     frappe.call({

//     //         method:"infac.infac.page.hr_dashboard.hr_dashboard.get_late_employees",

//     //         callback:function(r){

//     //             let data = r.message || [];

//     //             let html = `
//     //                 <table class="table table-bordered">
//     //                     <thead>
//     //                         <tr>
//     //                             <th>Employee</th>
//     //                             <th>Name</th>
//     //                             <th>Shift</th>
//     //                             <th>Checkin Time</th>
//     //                             <th>Employment</th>
//     //                         </tr>
//     //                     </thead>
//     //                     <tbody>
//     //             `;

//     //             data.forEach(emp=>{

//     //                 html += `
//     //                     <tr>
//     //                         <td>${emp.employee}</td>
//     //                         <td>${emp.employee_name}</td>
//     //                         <td>${emp.shift || ""}</td>
//     //                         <td>${frappe.datetime.str_to_user(emp.time)}</td>
//     //                         <td>${emp.employment_type || ""}</td>
//     //                     </tr>
//     //                 `;

//     //             });

//     //             html += `</tbody></table>`;


//     //             let d = new frappe.ui.Dialog({

//     //                 title:"Late Employees",

//     //                 fields:[
//     //                     {
//     //                         fieldtype:"HTML",
//     //                         fieldname:"table_html"
//     //                     }
//     //                 ]

//     //             });

//     //             d.fields_dict.table_html.$wrapper.html(html);

//     //             d.show();

//     //         }

//     //     });

//     // }

//     function show_late_employees(){
//         const from_date = $("#late-from-date").val();
//         const to_date = $("#late-to-date").val();
//         frappe.call({
//             method:"infac.infac.page.hr_dashboard.hr_dashboard.get_late_employees",
//              args:{
//             from_date:from_date,
//             to_date:to_date
//         },
//             callback:function(r){

//                 let data = r.message || [];

//                 let html = `

//                     <div style="text-align:right;margin-bottom:10px;">
//                         <button class="btn btn-primary btn-sm" id="download-late-btn">
//                             Download Excel
//                         </button>
//                     </div>

//                     <table class="table table-bordered">
//                         <thead>
//                             <tr>
//                                 <th>Employee</th>
//                                 <th>Name</th>
//                                 <th>Shift</th>
//                                 <th>Checkin Time</th>
//                                 <th>Employment</th>
//                             </tr>
//                         </thead>
//                         <tbody>
//                 `;

//                 data.forEach(emp=>{

//                     html += `
//                         <tr>
//                             <td>${emp.employee}</td>
//                             <td>${emp.employee_name}</td>
//                             <td>${emp.shift || ""}</td>
//                             <td>${frappe.datetime.str_to_user(emp.time)}</td>
//                             <td>${emp.employment_type || ""}</td>
//                         </tr>
//                     `;

//                 });

//                 html += `</tbody></table>`;


//                 let d = new frappe.ui.Dialog({
//                     title:"Late Employees",
//                     size: "large",
//                     fields:[
//                         {
//                             fieldtype:"HTML",
//                             fieldname:"table_html"
//                         }
//                     ]
//                 });

//                 d.fields_dict.table_html.$wrapper.html(html);

//                 d.show();

//             }
//         });
// }


// function download_late_excel(){

//     const from_date = $("#late-from-date").val();
//     const to_date = $("#late-to-date").val();

//     window.open(
//         `/api/method/infac.infac.page.hr_dashboard.hr_dashboard.download_late_excel?from_date=${from_date}&to_date=${to_date}`
//     );

// }

// 	$(wrapper).on('click', '#apply-filter', function() {
//         loadData();
// 		loadLeaveSummary();
// 		loadHeadCountDetails();
//         loadLateSummary();
//         load_late_count();
//         loadDeptLineSummary();
//     });
//     loadData();
//     loadLateSummary();
//     load_late_count();
//     loadDeptLineSummary();

// 	function loadLeaveSummary() {
// 		let selected_date = document.getElementById("filter-date").value || frappe.datetime.get_today();

// 		frappe.call({
// 			method: "infac.infac.page.hr_dashboard.hr_dashboard.get_leave_summary",
// 			args: { attendance_date: selected_date },
// 			callback: function(r) {
// 				if (r.message) {
// 					let data = r.message;

// 					let circle = document.querySelector(".leave-circle");
// 					// Update gradient
//                     circle.style.background = `conic-gradient(
//                         #95e0e5ff 0% ${data.approved_pct}%,
//                         #F44336 ${data.approved_pct}% 100%
//                     )`;

//                     // Update text inside circle
//                     circle.querySelector(".approved-text").innerText = `${data.approved_pct}% Approved`;
//                     circle.querySelector(".unapproved-text").innerText = `${data.unapproved_pct}% Unapproved`;

//                     // Update bottom labels if needed
//                     let labelBox = document.querySelector(".leave-label");
//                     labelBox.innerHTML = `<div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px; font-size: 14px;">
//                         <div><span style="color:#4CAF50; font-weight:bold;">●</span> Approved: ${data.approved}</div>
//                         <div><span style="color:#F44336; font-weight:bold;">●</span> Unapproved: ${data.unapproved}</div>
//                     </div>`;


// 				}
// 			}
// 		});
// 	}

// 	loadLeaveSummary();
// 	loadHeadCountDetails();

//     function loadHeadCountDetails() {
//         let selected_date = document.getElementById("filter-date").value || frappe.datetime.get_today();
//         let selected_shift = document.getElementById("shift").value || "All";

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard.hr_dashboard.get_headcount_summary",
//             args: { attendance_date: selected_date, shift: selected_shift },
//             callback: function(r) {
//                     if (!r.message) return;

//                     let tbody = document.getElementById("dept-summary-body");
//                     tbody.innerHTML = "";

//                     Object.keys(r.message).forEach(dept => {
//                         let d = r.message[dept];

//                         let overall = d.overall || { avail: 0, present: 0, absent: 0 };

//                         let absent_pct = overall.avail
//                             ? ((overall.absent / overall.avail) * 100).toFixed(0)
//                             : 0;

//                         let tr = document.createElement("tr");

//                         tr.innerHTML = `
//                             <td>${dept}</td>

//                             <td>${overall.avail}</td>
//                             <td style="color:green">${overall.present}</td>
//                             <td style="color:red">${overall.absent}</td>
//                             <td><b>${absent_pct}%</b></td>

//                             ${shiftCols(d["1st Shift"])}
//                             ${shiftCols(d["General"])}
//                             ${shiftCols(d["2nd Shift"])}
//                             ${shiftCols(d["3rd Shift"])}
//                         `;

//                         tbody.appendChild(tr);
//                     });
//                 }

//         });
//     }

//     function shiftCols(s) {
//     s = s || { plan: 0, present: 0, absent: 0 };

//     return `
//         <td>${s.plan}</td>
//         <td style="color:green">${s.present}</td>
//         <td style="color:red">${s.absent}</td>
//     `;
// }


//     function loadContractorSummary(date) {
//             let selected_shift = document.getElementById("shift").value || "All";

//             frappe.call({
//                 method: "infac.infac.page.hr_dashboard.hr_dashboard.get_contractor_summary",
//                args: { attendance_date: date, shift: selected_shift },
//             callback: function(r) {
//                 if (r.message) {
//                     let tbody = document.getElementById("late-reason-body");
//                     tbody.innerHTML = "";

//                     r.message.forEach(row => {
//                         let tr = `
//                             <tr ${row.contractor === "Total" ? 'style="font-weight:bold;background:#f1f1f1;"' : ''}>
//                                 <td style="text-align:left;">${row.contractor || '-'}</td>
//                                 <td style="text-align:center;">${row.enrolled}</td>
//                                 <td style="text-align:center;">${row.present}</td>
//                                 <td style="text-align:center;">${row.absent}</td>
//                             </tr>`;
//                         tbody.innerHTML += tr;
//                     });
//                 }
//             }
//         });
//     }

//     document.getElementById("apply-filter").addEventListener("click", function () {
//         let date = document.getElementById("filter-date").value;
//         loadContractorSummary(date);
//     });

//     window.addEventListener("load", function () {
//         let today = new Date().toISOString().split("T")[0];
//         document.getElementById("filter-date").value = today;
//         loadContractorSummary(today);
//     });


//     const s = document.createElement('script');
// s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';

// s.onload = function () {

//     // 🔹 LOAD DATALABEL PLUGIN
//     const dl = document.createElement('script');
//     dl.src = 'https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2';

//     dl.onload = function () {

//         let chartInstance = null;

//         function fetchWeeklyAttendance(from_date, to_date) {
//             frappe.call({
//                 method: "infac.infac.page.hr_dashboard.hr_dashboard.get_weekly_attendance",
//                 args: { from_date, to_date },
//                 callback: function (r) {
//                     if (!r.message) return;

//                     const data = r.message;
//                     const labels = data.map(d => d.date);
//                     const percent = data.map(d => Number(d.percent) || 0);

//                     // TABLE
//                     let rows = "";
//                     data.forEach(d => {
//                         rows += `
//                             <tr>
//                                 <td style="text-align:center;background:#f5f5f5;">${d.date}</td>
//                                 <td style="text-align:center;">${d.plan}</td>
//                                 <td style="text-align:center;">${d.actual}</td>
//                                 <td style="text-align:center;">${d.gap}</td>
//                                 <td style="text-align:center;">${d.percent}%</td>
//                             </tr>`;
//                     });
//                     $('#weekly-attendance-body').html(rows);

//                     const ctx = document
//                         .getElementById('weeklyAttendanceChart')
//                         .getContext('2d');

//                     if (chartInstance) chartInstance.destroy();

//                     chartInstance = new Chart(ctx, {
//                         type: 'line',
//                         data: {
//                             labels: labels,
//                             datasets: [{
//                                 label: '% Attendance',
//                                 data: percent,
//                                 borderWidth: 2,
//                                 tension: 0.3,
//                                 pointRadius: 4
//                             }]
//                         },
//                         options: {
//                             plugins: {
//                                     datalabels: {
//                                         display: true,
//                                         align: 'top',
//                                         anchor: 'end',
//                                         offset: 4,
//                                         clip: false,      
//                                         clamp: true, 
//                                         font: {
//                                             weight: 'bold',
//                                             size: 11
//                                         },
//                                         formatter: function (value) {
//                                             return value + '%'; 
//                                         }
//                                     }
//                                 },

//                             scales: {
//                                 y: {
//                                     beginAtZero: true,
//                                     title: { display: true, text: 'Percentage (%)' }
//                                 },
//                                 x: {
//                                     title: { display: true, text: 'Date' }
//                                 }
//                             }
//                         },
//                         plugins: [ChartDataLabels]
//                     });
//                 }
//             });
//         }

//         setDefaultWeekDates();
//         // DEFAULT LOAD
//         const formatDate = d => d.toISOString().split('T')[0];
//         const today = new Date();
//         const next6 = new Date();
//         next6.setDate(today.getDate() + 6);

//         fetchWeeklyAttendance(formatDate(today), formatDate(next6));

//         // APPLY BUTTON
//         $('#apply-weekly-filter').on('click', function () {
//             const from_date = $('#from-date').val();
//             const to_date = $('#to-date').val();

//             if (!from_date || !to_date) {
//                 frappe.msgprint("Please select both From and To dates");
//                 return;
//             }
//             fetchWeeklyAttendance(from_date, to_date);
//         });
//     };

//     document.head.appendChild(dl);
// };
// document.head.appendChild(s);
// };

// $(document).on("click", ".click-present", async function () {
//     const dept = String($(this).data("dept")).trim();
//     const date = $(this).data("date");

//     // Step 2: Route to Employee Checkin
//     frappe.set_route("Report", "Employee Checkin", {
        
//         log_type: "IN",
//         department: dept,
//         time: ["between", [
//             date + " 00:00:00",
//             date + " 23:59:59"
//         ]]
//     });
// });

// $(document).on("click", ".click-plan", async function () {
//     const dept = String($(this).data("dept")).trim();
//     const date = $(this).data("date");

//     // let employees = await frappe.db.get_list("Employee", {
//     //     filters: { department: dept },
//     //     pluck: "name"
//     // });

//     // let emp_list = employees.map(e => e.name);

//     frappe.set_route("Report", "Shift Assignment", {
//         department: dept,
//         start_date: ["<=", date],
//         end_date: [">=", date],
//         docstatus: 1
//     });
// });

// function setDefaultWeekDates() {
//     const today = new Date();

//     let day = today.getDay(); 
//     let diffToMonday = day === 0 ? -6 : 1 - day;

//     let monday = new Date(today);
//     monday.setDate(today.getDate() + diffToMonday);

//     let saturday = new Date(monday);
//     saturday.setDate(monday.getDate() + 5);

//     const formatDate = (date) => {
//         return date.toISOString().split('T')[0];
//     };

//     $('#from-date').val(formatDate(monday));
//     $('#to-date').val(formatDate(saturday));
// }

frappe.pages['hr-dashboard'].on_page_load = function(wrapper) {

    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'HR Dashboard',
        single_column: true
    });

    frappe.breadcrumbs.add('infac');

    // =========================================================
    // CSS
    // =========================================================

    const style = document.createElement('style');

    style.innerHTML = `

        .page-content-wrapper {
            display: flex;
            justify-content: center;
        }

        .dashboard-wrapper {
            width: 80%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f7fb;
        }

        @media (max-width: 1400px) {
            .dashboard-wrapper {
                width: 75%;
            }
        }

        @media (max-width: 1100px) {
            .dashboard-wrapper {
                width: 90%;
            }
        }

        @media (max-width: 768px) {
            .dashboard-wrapper {
                width: 100%;
                padding: 12px;
            }
        }

        .page-header {
            text-align: center;
            margin-bottom: 20px;
        }

        .filter-bar {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 12px;
        }

        .hr-layout {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .hr-card {
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            padding: 16px;
            border: 1px solid #e5e7eb;
            width: 100%;
        }

        .hr-card h3 {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .hr-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        .hr-table thead th {
            background: #f3f4f6;
            padding: 8px;
            border-bottom: 1px solid #e5e7eb;
            text-align: center;
            font-weight: 600;
        }

        .hr-table td {
            padding: 8px;
            border-bottom: 1px solid #f1f5f9;
        }

        .hr-table td:first-child,
        .hr-table th:first-child {
            text-align: left;
        }

        .hr-table tbody tr:hover {
            background: #f9fafb;
        }

        .dashboard-cards {
            display: flex;
            gap: 20px;
            margin-top: 25px;
            flex-wrap: wrap;
        }

        .custom-card {
            flex: 1;
            min-width: 220px;
            padding: 20px;
            border-radius: 14px;
            color: #fff;
            cursor: pointer;
            transition: 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .custom-card h4 {
            margin: 0;
            font-size: 15px;
            font-weight: 500;
            opacity: 0.9;
        }

        .custom-card h2 {
            margin-top: 10px;
            font-size: 28px;
            font-weight: 600;
        }

        .custom-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        .center {
            text-align: center;
        }

        .muted {
            color: #64748b;
        }

        .click-count {
            cursor: pointer;
            color: #2563eb;
            font-weight: 700;
            text-decoration: underline;
        }

        .click-count:hover {
            color: #1d4ed8;
        }

        .click-plan,
        .click-present {
            cursor: pointer;
            font-weight: 600;
        }

        .click-plan:hover,
        .click-present:hover {
            text-decoration: underline;
        }

        .dept-card {
            background: #fff;
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,.08);
            transition: .2s ease;
        }

        .dept-card:hover {
            transform: translateY(-3px);
        }

        .dept-title {
            font-weight: 600;
            margin-bottom: 10px;
        }

        .dept-stat {
            display: flex;
            justify-content: space-between;
            margin: 6px 0;
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
        }

        .stat-available {
            background: #eef4ff;
        }

        .stat-present {
            background: #e9f9ee;
        }

        .stat-absent {
            background: #ffecec;
        }

        .dept-stat:hover {
            opacity: 0.85;
        }

        .total-click {
            cursor: pointer;
            color: #2563eb;
            font-weight: 700;
            text-decoration: underline;
        }

        .total-click:hover {
            color: #1d4ed8;
        }

        #cal-emp-id-wrap .form-group {
            margin-bottom: 0;
            width: 100%;
        }

        #cal-emp-id-wrap .control-input,
        #cal-emp-id-wrap .awesomplete {
            width: 100%;
        }

        #cal-emp-id-wrap .form-control {
            height: 38px;
        }

        #cal-emp-id-wrap .awesomplete > ul {
            z-index: 100;
        }

       /* ---------- dark card ---------- */
#cal-card {
    background: #14171c;
    border-color: #262b33;
    color: #e5e7eb;
}
#cal-card h3 { color: #f1f5f9; }
#cal-card .form-control {
    background: #1d2229;
    border: 1px solid #2b323c;
    color: #e5e7eb;
}
#cal-card .form-control::placeholder { color: #6b7480; }
#cal-card .form-control:focus { border-color: #38bdf8; box-shadow: none; }
/* ---------- light card ---------- */
#cal-card {
    background: #ffffff;
    border-color: #e5e7eb;
    color: #1f2937;
}
#cal-card h3 { color: #0f172a; }
#cal-card .form-control {
    background: #f4f6f9;
    border: 1px solid #e2e8f0;
    color: #1f2937;
}
#cal-card .form-control::placeholder { color: #94a3b8; }
#cal-card .form-control:focus {
    background: #fff;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15);
}

.cal-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 10px;
    color: #475569;
    font-size: 13px;
}
.cal-toolbar b { color: #2563eb; }

.cal-legend {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #64748b;
}
.cal-legend .cal-chip {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: inline-block;
}

/* ---------- table ---------- */
.cal-scroll {
    max-height: 560px;
    overflow: auto;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}
.cal-table {
    border-collapse: separate;
    border-spacing: 0;
    font-size: 13px;
    width: 100%;
    min-width: 980px;
}
.cal-table th,
.cal-table td {
    padding: 9px 10px;
    border-bottom: 1px solid #eef1f5;
    border-right: 1px solid #f3f5f8;
    background: #ffffff;
    color: #1f2937;
}
.cal-table thead th {
    position: sticky;
    top: 0;
    z-index: 3;
    background: #f1f5f9;
    font-weight: 600;
    font-size: 12px;
    color: #475569;
    text-align: center;
    white-space: nowrap;
    border-bottom: 1px solid #e2e8f0;
}
.cal-table tfoot td {
    position: sticky;
    bottom: 0;
    z-index: 3;
    background: #f1f5f9;
    border-top: 1px solid #e2e8f0;
}

/* sticky ID + Name columns */
.cal-table .cal-col-id,
.cal-table .cal-col-name {
    position: sticky;
    z-index: 2;
    text-align: left;
    white-space: nowrap;
}
.cal-table .cal-col-id {
    left: 0;
    min-width: 100px;
    box-shadow: inset 4px 0 0 var(--stripe, #3b82f6);
    padding-left: 14px;
}
.cal-table .cal-col-name {
    left: 100px;
    min-width: 190px;
    box-shadow: 2px 0 4px -2px rgba(0,0,0,.15);
}
.cal-table thead .cal-col-id,
.cal-table thead .cal-col-name,
.cal-table tfoot .cal-col-id,
.cal-table tfoot .cal-col-name { z-index: 4; }
.cal-table tfoot .cal-col-id { box-shadow: none; }

.cal-table tbody tr:nth-child(even) td { background: #fafbfd; }
.cal-table tbody tr:hover td {
    background: #eaf3ff;
    border-top: 1px solid #93c5fd;
    border-bottom: 1px solid #93c5fd;
}

/* ---------- employee + avatar ---------- */
.cal-emp { display: flex; align-items: center; gap: 8px; }
.cal-avatar {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* ---------- cells ---------- */
.cal-cell { text-align: center; min-width: 56px; }
.cal-cell.cal-current-month {
    background-image: linear-gradient(rgba(59,130,246,.07), rgba(59,130,246,.07));
}
.cal-empty { color: #cbd5e1 !important; }

.cal-badge {
    display: inline-block;
    width: 26px;
    height: 26px;
    line-height: 26px;
    border-radius: 50%;
    text-align: center;
    font-weight: 700;
    font-size: 12px;
    cursor: default;
    box-shadow: 0 1px 3px rgba(15,23,42,.25);
}

.cal-total {
    text-align: center;
    font-weight: 700;
    color: #0f172a !important;
    border-left: 1px solid #e2e8f0;
}

/* ---------- badge colours ---------- */
.cal-theme-Permission { --c2:#fcd34d; --c3:#f59e0b; --c4:#c2410c; }
.cal-theme-Leave      { --c2:#86efac; --c3:#22c55e; --c4:#15803d; }
.cal-theme-Late       { --c2:#fca5a5; --c3:#ef4444; --c4:#b91c1c; }
.cal-theme-All        { --c2:#93c5fd; --c3:#3b82f6; --c4:#1d4ed8; }

.cal-lv1 { background: #e2e8f0; color: #334155; }
.cal-lv2 { background: var(--c2); color: #1f2937; }
.cal-lv3 { background: var(--c3); color: #fff; }
.cal-lv4 { background: var(--c4); color: #fff; }
    `;

    document.head.appendChild(style);


    // =========================================================
    // HTML
    // =========================================================

    $(wrapper).html(`

        <div class="dashboard-wrapper">

            <div class="page-header">

                <h2>HR Dashboard</h2>

            </div>

            <div class="hr-layout">

                <!-- TOP CARDS -->

                <div class="dashboard-cards">

                    <div
                        class="custom-card"
                        id="late-toggle-card"
                        style="background:linear-gradient(135deg,#4facfe,#00f2fe);"
                    >

                        <img
                            src="/assets/infac/images/late.png"
                            style="width:36px;height:36px;object-fit:contain;"
                            onerror="this.style.display='none'"
                        >

                        <h4>Late Employees</h4>

                        <h2 id="late-card-count">0</h2>

                    </div>


                    <div
                        class="custom-card"
                        id="perm-toggle-card"
                        style="background:linear-gradient(135deg,#f7971e,#ffd200);"
                    >

                        <img
                            src="/assets/infac/images/permission.png"
                            style="width:36px;height:36px;object-fit:contain;"
                            onerror="this.style.display='none'"
                        >

                        <h4>Permission Employees</h4>

                        <h2 id="perm-card-count">0</h2>

                    </div>


                    <div
                        class="custom-card"
                        id="leave-toggle-card"
                        style="background:linear-gradient(135deg,#43cea2,#185a9d);"
                    >

                        <img
                            src="/assets/infac/images/leave.png"
                            style="width:36px;height:36px;object-fit:contain;"
                            onerror="this.style.display='none'"
                        >

                        <h4>Leave Employees</h4>

                        <h2 id="leave-card-count">0</h2>

                    </div>

                </div>


                <!-- =====================================================
                     MAIN FILTER
                     MOVED HERE - BELOW THE 3 CARDS
                     ===================================================== -->

                <div class="filter-bar">

                    <input
                        type="date"
                        id="filter-date"
                        class="form-control"
                        style="width:200px;"
                    >

                    <select
                        id="shift"
                        class="form-control"
                        style="width:200px;"
                    >
                        <option value="All">All Shift</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="G">G</option>
                    </select>

                    <button
                        id="apply-filter"
                        class="btn btn-primary"
                    >
                        Apply
                    </button>

                </div>


                <!-- LATE ENTRY DETAILS -->

                <div
                    class="row"
                    id="late-entry-section"
                    style="display:none;"
                >

                    <div class="col-md-12">

                        <div class="hr-card">

                            <div
                                style="
                                    display:flex;
                                    justify-content:space-between;
                                    align-items:center;
                                    margin-bottom:10px;
                                "
                            >

                                <h3 style="margin:0;">
                                    Late Entry Details
                                </h3>

                                <div style="display:flex;gap:8px;">

                                    <input
                                        type="date"
                                        id="late-from-date"
                                        class="form-control"
                                        style="width:150px;"
                                    >

                                    <input
                                        type="date"
                                        id="late-to-date"
                                        class="form-control"
                                        style="width:150px;"
                                    >

                                    <button
                                        class="btn btn-primary btn-sm"
                                        id="late-filter-btn"
                                    >
                                        Apply
                                    </button>

                                </div>

                            </div>

                            <div class="table-responsive">

                                <table
                                    class="hr-table"
                                    id="late-summary-table"
                                >

                                    <thead>

                                        <tr>
                                            <th>Shift/Category</th>
                                            <th>Staff</th>
                                            <th>Worker</th>
                                            <th>NAPS</th>
                                            <th>Contract</th>
                                            <th>Trainee</th>
                                        </tr>

                                    </thead>

                                    <tbody id="late-summary-body">

                                        <tr>

                                            <td
                                                colspan="6"
                                                style="
                                                    text-align:center;
                                                    padding:16px;
                                                "
                                            >
                                                Loading...
                                            </td>

                                        </tr>

                                    </tbody>

                                </table>

                            </div>

                        </div>

                    </div>

                </div>


                <!-- PERMISSION SUMMARY -->

                <div
                    class="row"
                    id="permission-section"
                    style="display:none;"
                >

                    <div class="col-md-12">

                        <div
                            class="hr-card"
                            id="permission-summary-card"
                        >

                            <div
                                style="
                                    display:flex;
                                    justify-content:space-between;
                                    align-items:center;
                                    margin-bottom:12px;
                                "
                            >

                                <h3 style="margin:0;">
                                    Permission Summary
                                </h3>

                                <div style="display:flex;gap:8px;">

                                    <input
                                        type="date"
                                        id="perm-from-date"
                                        class="form-control"
                                        style="width:150px;"
                                    >

                                    <input
                                        type="date"
                                        id="perm-to-date"
                                        class="form-control"
                                        style="width:150px;"
                                    >

                                    <button
                                        class="btn btn-primary btn-sm"
                                        id="perm-filter-btn"
                                    >
                                        Apply
                                    </button>

                                </div>

                            </div>

                            <table class="table table-bordered">

                                <thead>

                                    <tr
                                        style="
                                            background-color:#e9ecef;
                                            color:#333;
                                            font-weight:600;
                                        "
                                    >

                                        <th>Shift/Category</th>
                                        <th>Staff</th>
                                        <th>Worker</th>
                                        <th>NAPS</th>
                                        <th>Contract</th>
                                        <th>Trainee</th>

                                    </tr>

                                </thead>

                                <tbody id="perm-summary-body"></tbody>

                            </table>

                        </div>

                    </div>

                </div>


                <!-- LEAVE SUMMARY -->

                <div
                    id="leave-summary-section"
                    style="display:none;"
                >

                    <div
                        class="hr-card"
                        id="leave-summary-card"
                    >

                        <h3>Leave Summary</h3>

                        <div
                            style="
                                display:flex;
                                justify-content:flex-start;
                                align-items:center;
                                margin-bottom:12px;
                            "
                        >

                            <div
                                style="
                                    display:flex;
                                    gap:10px;
                                    align-items:center;
                                "
                            >

                                <input
                                    type="date"
                                    id="leave-from-date"
                                    class="form-control"
                                    style="width:180px;"
                                >

                                <input
                                    type="date"
                                    id="leave-to-date"
                                    class="form-control"
                                    style="width:180px;"
                                >

                                <button
                                    class="btn btn-primary btn-sm"
                                    id="leave-filter-btn"
                                >
                                    Apply
                                </button>

                                <button
                                    class="btn btn-success btn-sm"
                                    id="leave-download-btn"
                                >
                                    Download
                                </button>

                            </div>

                        </div>

                        <div id="leave-detail-table"></div>

                    </div>

                </div>


                <!-- HEAD COUNT -->

                <div class="hr-card">

                    <h3>Head Count Details</h3>

                    <div class="table-responsive">

                        <table class="hr-table">

                            <thead>

                                <tr>

                                    <th rowspan="2">
                                        Department
                                    </th>

                                    <th colspan="4">
                                        Overall
                                    </th>

                                    <th colspan="3">
                                        1st Shift
                                    </th>

                                    <th colspan="3">
                                        General Shift
                                    </th>

                                    <th colspan="3">
                                        2nd Shift
                                    </th>

                                    <th colspan="3">
                                        3rd Shift
                                    </th>

                                </tr>

                                <tr>

                                    <th>Avail</th>
                                    <th>Present</th>
                                    <th>Absent</th>
                                    <th>%</th>

                                    <th>Plan</th>
                                    <th>Present</th>
                                    <th>Absent</th>

                                    <th>Plan</th>
                                    <th>Present</th>
                                    <th>Absent</th>

                                    <th>Plan</th>
                                    <th>Present</th>
                                    <th>Absent</th>

                                    <th>Plan</th>
                                    <th>Present</th>
                                    <th>Absent</th>

                                </tr>

                            </thead>

                            <tbody id="dept-summary-body"></tbody>

                        </table>

                    </div>

                </div>


                <!-- TRANSACTION CALENDAR -->

                <div class="hr-card" id="cal-card">

                    <div
                        style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            margin-bottom:12px;
                            flex-wrap:wrap;
                            gap:10px;
                        "
                    >

                        <h3 style="margin:0;">
                            Leave, Late and Permission Calendar
                        </h3>

                        <button
                            class="btn btn-success btn-sm"
                            id="cal-download-btn"
                        >
                            Download
                        </button>

                    </div>

                    <div
                        class="filter-bar"
                        style="
                            justify-content:flex-start;
                            margin-top:0;
                            margin-bottom:12px;
                        "
                    >

                        <select
                            id="cal-app"
                            class="form-control"
                            style="width:180px;"
                        >
                            <option value="All">
                                All Applications
                            </option>
                            <option value="Leave">
                                Leave
                            </option>
                            <option value="Late">
                                Late
                            </option>
                            <option value="Permission">
                                Permission
                            </option>
                        </select>

                        <select
                            id="cal-emp-type"
                            class="form-control"
                            style="width:180px;"
                        >
                            <option value="All">
                                All Employee Types
                            </option>
                            <option value="Staff">
                                Staff
                            </option>
                            <option value="Worker">
                                Worker
                            </option>
                            <option value="NAPS">
                                NAPS
                            </option>
                            <option value="Contract">
                                Contract
                            </option>
                            <option value="Trainee">
                                Trainee
                            </option>
                        </select>

                        <input
                            type="date"
                            id="cal-from-date"
                            class="form-control"
                            style="width:160px;"
                        >

                        <input
                            type="date"
                            id="cal-to-date"
                            class="form-control"
                            style="width:160px;"
                        >

                        <div
                            id="cal-emp-id-wrap"
                            style="
                                width:230px;
                                display:flex;
                                align-items:center;
                            "
                        ></div>

                    </div>

                    <div id="cal-container">

                        <div
                            class="center muted"
                            style="padding:16px;"
                        >
                            Choose filter
                        </div>

                    </div>

                </div>


                <!-- WEEKLY ATTENDANCE -->

                <div class="row">

                    <div class="col-md-6">

                        <div class="hr-card">

                            <h3>
                                Weekly Attendance Summary Graph
                            </h3>

                            <div
                                class="filter-bar"
                                style="
                                    display:flex;
                                    gap:10px;
                                    margin-bottom:10px;
                                "
                            >

                                <input
                                    type="date"
                                    id="from-date"
                                    class="form-control"
                                    style="width:180px;"
                                >

                                <input
                                    type="date"
                                    id="to-date"
                                    class="form-control"
                                    style="width:180px;"
                                >

                                <button
                                    id="apply-weekly-filter"
                                    class="btn btn-primary"
                                >
                                    Apply
                                </button>

                            </div>

                            <canvas
                                id="weeklyAttendanceChart"
                                height="120"
                            ></canvas>

                        </div>

                    </div>


                    <div class="col-md-6">

                        <div class="hr-card">

                            <h3>
                                Weekly Attendance Summary Table
                            </h3>

                            <div class="table-responsive">

                                <table class="hr-table">

                                    <thead>

                                        <tr>
                                            <th>Date</th>
                                            <th>Plan</th>
                                            <th>Actual</th>
                                            <th>Gap</th>
                                            <th>%</th>
                                        </tr>

                                    </thead>

                                    <tbody
                                        id="weekly-attendance-body"
                                    ></tbody>

                                </table>

                            </div>

                        </div>

                    </div>

                </div>


                <!-- CONTRACTOR SUMMARY -->

                <div class="hr-card">

                    <h3>
                        Contractor Wise Attendance
                    </h3>

                    <div class="table-responsive">

                        <table class="hr-table">

                            <thead>

                                <tr>
                                    <th>Contractor Name</th>
                                    <th>Available</th>
                                    <th>Present</th>
                                    <th>Absent</th>
                                </tr>

                            </thead>

                            <tbody id="late-reason-body">

                                <tr>

                                    <td
                                        colspan="4"
                                        class="center"
                                    >
                                        Loading...
                                    </td>

                                </tr>

                            </tbody>

                        </table>

                    </div>

                </div>


                <!-- DEPARTMENT LINE SUMMARY -->

                <div class="hr-card">

                    <div
                        class="d-flex justify-content-between align-items-center mb-2"
                    >

                        <h3 class="mb-0">
                            Department Line Summary
                        </h3>

                        <button
                            class="btn btn-sm btn-success"
                            id="download-dept-line"
                        >
                            Download
                        </button>

                    </div>

                    <div class="table-responsive">

                        <table
                            id="dept_line_summary"
                            class="hr-table"
                        >

                            <thead>

                                <tr>

                                    <th>Department Line</th>
                                    <th>Available</th>
                                    <th>Present</th>
                                    <th>Absent</th>
                                    <th>Absent %</th>

                                </tr>

                            </thead>

                            <tbody></tbody>

                        </table>

                    </div>

                </div>


            </div>

        </div>

    `);


    // =========================================================
    // DEFAULT DATES
    // =========================================================

    const today = frappe.datetime.get_today();

    $(wrapper).find("#filter-date").val(today);

    $(wrapper).find("#late-from-date").val(today);
    $(wrapper).find("#late-to-date").val(today);

    $(wrapper).find("#perm-from-date").val(today);
    $(wrapper).find("#perm-to-date").val(today);

    $(wrapper).find("#leave-from-date").val(today);
    $(wrapper).find("#leave-to-date").val(today);

    $(wrapper).find("#late-entry-section").hide();
    $(wrapper).find("#permission-section").hide();
    $(wrapper).find("#leave-summary-section").hide();


    // =========================================================
    // TRANSACTION CALENDAR (MONTH-WISE)
    // =========================================================

    const cal_current_year =
        new Date().getFullYear();

    $(wrapper)
        .find("#cal-from-date")
        .val(`${cal_current_year}-01-01`);

    $(wrapper)
        .find("#cal-to-date")
        .val(`${cal_current_year}-12-31`);


    const cal_emp_control =
        frappe.ui.form.make_control({

            parent:
                $(wrapper)
                    .find("#cal-emp-id-wrap"),

            only_input: true,

            df: {

                fieldtype:
                    "Link",

                options:
                    "Employee",

                fieldname:
                    "cal_emp_id",

                placeholder:
                    "Employee ID",

                change: function() {

                    loadTxnCalendar();

                }

            },

            render_input: true

        });


    // function renderTxnCalendar(
    //     employees,
    //     year
    // ) {

    //     if (!employees.length) {

    //         return `

    //             <div
    //                 class="center muted"
    //                 style="padding:20px;"
    //             >
    //                 No transactions found
    //             </div>

    //         `;

    //     }

    //     const months = [
    //         "Jan",
    //         "Feb",
    //         "Mar",
    //         "Apr",
    //         "May",
    //         "Jun",
    //         "Jul",
    //         "Aug",
    //         "Sep",
    //         "Oct",
    //         "Nov",
    //         "Dec"
    //     ];

    //     const pad = n =>
    //         String(n).padStart(2, "0");

    //     let header = `

    //         <tr>
    //             <th>Employee ID</th>
    //             <th>Employee Name</th>
    //     `;

    //     months.forEach(function(m) {

    //         header += `<th>${m}</th>`;

    //     });

    //     header += `</tr>`;

    //     let body = "";

    //     employees.forEach(function(emp) {

    //         const days = emp.days || {};

    //         body += `

    //             <tr>

    //                 <td>
    //                     ${frappe.utils.escape_html(
    //                         String(
    //                             emp.employee_id || ""
    //                         )
    //                     )}
    //                 </td>

    //                 <td>
    //                     ${frappe.utils.escape_html(
    //                         String(
    //                             emp.employee_name || ""
    //                         )
    //                     )}
    //                 </td>

    //         `;

    //         for (let m = 0; m < 12; m++) {

    //             const prefix =
    //                 `${year}-${pad(m + 1)}-`;

    //             const day_nums = [];

    //             let txn_count = 0;

    //             Object.keys(days).forEach(
    //                 function(k) {

    //                     if (
    //                         k.indexOf(prefix) === 0
    //                     ) {

    //                         const entries =
    //                             days[k];

    //                         txn_count +=
    //                             Array.isArray(entries)
    //                                 ? entries.length
    //                                 : 1;

    //                         const d =
    //                             parseInt(
    //                                 k.substring(8, 10),
    //                                 10
    //                             );

    //                         if (
    //                             day_nums.indexOf(d)
    //                             === -1
    //                         ) {
    //                             day_nums.push(d);
    //                         }

    //                     }

    //                 }
    //             );

    //             day_nums.sort(function(a, b) {
    //                 return a - b;
    //             });

    //             body += `

    //                 <td
    //                     class="cal-days"
    //                     title="${
    //                         txn_count
    //                             ? "Days: " +
    //                                 day_nums.join(" ")
    //                             : ""
    //                     }"
    //                 >
    //                     ${txn_count || ""}
    //                 </td>

    //             `;

    //         }

    //         body += `</tr>`;

    //     });

    //     return `

    //         <div class="table-responsive">

    //             <table class="cal-table">

    //                 <thead>${header}</thead>

    //                 <tbody>${body}</tbody>

    //             </table>

    //         </div>

    //     `;

    // }

function renderTxnCalendar(employees, from_date, to_date) {

    if (!employees.length) {
        return `<div class="center muted" style="padding:20px;">No transactions found</div>`;
    }

    const application = $(wrapper).find("#cal-app").val() || "All";

    const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    const pad = n => String(n).padStart(2, "0");
    const esc = v => frappe.utils.escape_html(String(v || ""));

    // month columns across the selected range
    const fy = parseInt(String(from_date).substring(0, 4), 10);
    const fm = parseInt(String(from_date).substring(5, 7), 10);
    const ty = parseInt(String(to_date).substring(0, 4), 10);
    const tm = parseInt(String(to_date).substring(5, 7), 10);

    const month_list = [];
    let cy = fy, cm = fm;
    while (cy < ty || (cy === ty && cm <= tm)) {
        month_list.push({ y: cy, m: cm });
        cm++;
        if (cm > 12) { cm = 1; cy++; }
    }

    const now = new Date();
    const cur_y = now.getFullYear();
    const cur_m = now.getMonth() + 1;

    const level = c => (c >= 7 ? 4 : c >= 4 ? 3 : c >= 2 ? 2 : 1);

    const hue = s => {
    let h = 0;
    String(s).split("").forEach(ch => { h = (h * 31 + ch.charCodeAt(0)) % 360; });
    return h;
};

    let header = `<tr>
        <th class="cal-col-id">Employee ID</th>
        <th class="cal-col-name">Employee Name</th>`;
    month_list.forEach(mi => {
        header += `<th>${months[mi.m - 1]} ${mi.y}</th>`;
    });
    header += `<th>Total</th></tr>`;

    let body = "";
    let shown = 0;
    const month_totals = new Array(month_list.length).fill(0);
    let grand_total = 0;

    employees.forEach(function (emp) {

        const id = String(emp.employee_id || "");
        const name = String(emp.employee_name || "");

        shown++;
        const days = emp.days || {};
        let row_total = 0;
        let cells = "";

        for (let i = 0; i < month_list.length; i++) {

            const mi = month_list[i];
            const prefix = `${mi.y}-${pad(mi.m)}-`;
            const day_nums = [];
            let count = 0;

            Object.keys(days).forEach(function (k) {
                if (k.indexOf(prefix) === 0) {
                    const entries = days[k];
                    count += Array.isArray(entries) ? entries.length : 1;
                    const d = parseInt(k.substring(8, 10), 10);
                    if (day_nums.indexOf(d) === -1) day_nums.push(d);
                }
            });

            day_nums.sort((a, b) => a - b);
            row_total += count;
            month_totals[i] += count;

            const cur = (mi.y === cur_y && mi.m === cur_m) ? " cal-current-month" : "";

            if (count) {
                cells += `
                    <td class="cal-cell${cur}">
                        <span class="cal-badge cal-lv${level(count)}"
                              title="${months[mi.m - 1]} ${mi.y} - Days: ${day_nums.join(", ")}">
                            ${count}
                        </span>
                    </td>`;
            } else {
                cells += `<td class="cal-cell cal-empty${cur}">&ndash;</td>`;
            }
        }

        grand_total += row_total;

                const hu = hue(id);

        body += `
            <tr style="--stripe:hsl(${hu} 65% 60%)">
                <td class="cal-col-id">${esc(id)}</td>
                <td class="cal-col-name">${esc(name)}</td>
                ${cells}
                <td class="cal-total">${row_total}</td>
            </tr>`;
    });

    if (!shown) {
        return `<div class="center muted" style="padding:20px;">No transactions found</div>`;
    }

    let footer = `<tr>
        <td class="cal-col-id cal-total"></td>
        <td class="cal-col-name cal-total" style="text-align:left;">Total</td>`;
    month_totals.forEach(t => {
        footer += `<td class="cal-total">${t || "&ndash;"}</td>`;
    });
    footer += `<td class="cal-total">${grand_total}</td></tr>`;

    return `
        <div class="cal-theme-${application}">

            <div class="cal-toolbar">
                <div style="font-size:13px;">
                    Employees: <b style="color:#2563eb;">${shown}</b>
                    &nbsp;|&nbsp;
                    Total transactions: <b style="color:#2563eb;">${grand_total}</b>
                </div>

                <div class="cal-legend">
                    <span>Fewer</span>
                    <span class="cal-chip cal-lv1" title="1"></span>
                    <span class="cal-chip cal-lv2" title="2-3"></span>
                    <span class="cal-chip cal-lv3" title="4-6"></span>
                    <span class="cal-chip cal-lv4" title="7+"></span>
                    <span>More</span>
                </div>
            </div>

            <div class="cal-scroll">
                <table class="cal-table">
                    <thead>${header}</thead>
                    <tbody>${body}</tbody>
                    <tfoot>${footer}</tfoot>
                </table>
            </div>

        </div>`;
}

    function loadTxnCalendar() {

        const application =
            $(wrapper)
                .find("#cal-app")
                .val() || "All";

        const employee_type =
            $(wrapper)
                .find("#cal-emp-type")
                .val() || "All";

        const employee_id =
            (
                cal_emp_control.get_value() || ""
            ).trim();

        const from_date =
            $(wrapper)
                .find("#cal-from-date")
                .val();

        const to_date =
            $(wrapper)
                .find("#cal-to-date")
                .val();

        const container =
            $(wrapper)
                .find("#cal-container");

        if (
            application === "All" &&
            employee_type === "All" &&
            !employee_id
        ) {

            container.html(`

                <div
                    class="center muted"
                    style="padding:20px;"
                >
                    Choose filter
                </div>

            `);

            return;

        }

        if (!from_date || !to_date) {

            container.html(`

                <div
                    class="center muted"
                    style="padding:20px;"
                >
                    Please select From Date and To Date
                </div>

            `);

            return;

        }

        if (from_date > to_date) {

            container.html(`

                <div
                    class="center muted"
                    style="padding:20px;"
                >
                    From Date cannot be greater than To Date
                </div>

            `);

            return;

        }

        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_txn_calendar",

            args: {

                application:
                    application,

                employee_type:
                    employee_type,

                employee_id:
                    employee_id,

                from_date:
                    from_date,

                to_date:
                    to_date

            },

            callback: function(r) {

                const response =
                    r.message || {};

                const employees =
                    Array.isArray(
                        response.employees
                    )
                        ? response.employees
                        : [];

                container.html(
                    renderTxnCalendar(
                        employees,
                        from_date,
                        to_date
                    )
                );

            },

            error: function(xhr) {

                console.error(
                    "Transaction Calendar Error:",
                    xhr
                );

                container.html(`

                    <div
                        class="center text-danger"
                        style="padding:20px;"
                    >
                        Error loading transaction calendar
                    </div>

                `);

            }

        });

    }


    $(wrapper).on(
        "change",
        "#cal-app, #cal-emp-type, #cal-from-date, #cal-to-date",
        function() {

            loadTxnCalendar();

        }
    );


    $(wrapper).on(
        "click",
        "#cal-download-btn",
        function() {

            const application =
                $(wrapper)
                    .find("#cal-app")
                    .val() || "All";

            const employee_type =
                $(wrapper)
                    .find("#cal-emp-type")
                    .val() || "All";

            const employee_id =
                (
                    cal_emp_control.get_value() ||
                    ""
                ).trim();

            const from_date =
                $(wrapper)
                    .find("#cal-from-date")
                    .val() || "";

            const to_date =
                $(wrapper)
                    .find("#cal-to-date")
                    .val() || "";

            if (
                application === "All" &&
                employee_type === "All" &&
                !employee_id
            ) {

                frappe.msgprint(
                    "Please choose a filter first"
                );

                return;

            }

            if (!from_date || !to_date) {

                frappe.msgprint(
                    "Please select From Date and To Date"
                );

                return;

            }

            window.open(
                `/api/method/infac.infac.page.hr_dashboard.hr_dashboard.download_txn_calendar` +
                `?application=${encodeURIComponent(application)}` +
                `&employee_type=${encodeURIComponent(employee_type)}` +
                `&employee_id=${encodeURIComponent(employee_id)}` +
                `&from_date=${encodeURIComponent(from_date)}` +
                `&to_date=${encodeURIComponent(to_date)}`
            );

        }
    );


    // =========================================================
    // TOP CARD CLICK
    // =========================================================

    $(wrapper).on("click", "#late-toggle-card", function() {

        $(wrapper)
            .find("#late-entry-section")
            .stop(true, true)
            .slideToggle(250);

    });


    $(wrapper).on("click", "#perm-toggle-card", function() {

        $(wrapper)
            .find("#permission-section")
            .stop(true, true)
            .slideToggle(250);

    });


    $(wrapper).on("click", "#leave-toggle-card", function() {

        $(wrapper)
            .find("#leave-summary-section")
            .stop(true, true)
            .slideToggle(250);

    });


    // =========================================================
    // PERMISSION SUMMARY
    // =========================================================

    function load_permission_summary() {

        const from_date =
            $(wrapper).find("#perm-from-date").val();

        const to_date =
            $(wrapper).find("#perm-to-date").val();

        if (!from_date || !to_date) {
            return;
        }

        frappe.call({

            method:
                "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_permission_summary",

            args: {
                from_date: from_date,
                to_date: to_date
            },

            callback: function(r) {

                const response = r.message || {};

                const data =
                    Array.isArray(response.summary)
                        ? response.summary
                        : [];

                const total =
                    Number(response.total) || 0;

                let html = "";

                data.forEach(row => {

                    const shift =
                        row.shift !== undefined &&
                        row.shift !== null
                            ? String(row.shift).trim()
                            : "";

                    html += `

                        <tr>

                            <td>
                                ${frappe.utils.escape_html(
                                    shift
                                )}
                            </td>

                            ${permissionCountCell(
                                row.staff,
                                "Staff",
                                shift
                            )}

                            ${permissionCountCell(
                                row.worker,
                                "Worker",
                                shift
                            )}

                            ${permissionCountCell(
                                row.naps,
                                "NAPS",
                                shift
                            )}

                            ${permissionCountCell(
                                row.contract,
                                "Contract",
                                shift
                            )}

                            ${permissionCountCell(
                                row.trainee,
                                "Trainee",
                                shift
                            )}

                        </tr>

                    `;

                });

                if (!data.length) {

                    html = `

                        <tr>

                            <td
                                colspan="6"
                                class="text-center"
                                style="padding:20px;"
                            >
                                No records found
                            </td>

                        </tr>

                    `;

                }

                $(wrapper)
                    .find("#perm-summary-body")
                    .html(html);

                $(wrapper)
                    .find("#perm-card-count")
                    .text(total);

            },

            error: function(xhr) {

                console.error(
                    "Permission Summary Error:",
                    xhr
                );

                $(wrapper)
                    .find("#perm-summary-body")
                    .html(`

                        <tr>

                            <td
                                colspan="6"
                                class="text-center text-danger"
                                style="padding:20px;"
                            >
                                Error loading permission summary
                            </td>

                        </tr>

                    `);

                $(wrapper)
                    .find("#perm-card-count")
                    .text("0");

            }

        });

    }


    // =========================================================
    // PERMISSION COUNT CELL
    // =========================================================

    function permissionCountCell(
        count,
        category,
        shift
    ) {

        const value =
            Number(count) || 0;

        if (!value) {

            return `

                <td class="text-center">
                    0
                </td>

            `;

        }

        const normalizedShift =
            String(shift || "")
                .trim()
                .toLowerCase();

        const isTotalShift =
            normalizedShift === "total" ||
            normalizedShift === "all";

        const safeCategory =
            frappe.utils.escape_html(
                String(category || "")
            );

        const safeShift =
            frappe.utils.escape_html(
                String(shift || "")
            );

        return `

            <td class="text-center">

                <span
                    class="
                        click-count
                        permission-count-click
                        ${isTotalShift ? "total-click" : ""}
                    "
                    data-category="${safeCategory}"
                    data-shift="${safeShift}"
                    data-count="${value}"
                    title="Click to view permission employees"
                >
                    ${value}
                </span>

            </td>

        `;

    }


    // =========================================================
    // PERMISSION FILTER
    // =========================================================

    $(wrapper).on(
        "click",
        "#perm-filter-btn",
        function() {

            load_permission_summary();

        }
    );


    // =========================================================
    // PERMISSION CATEGORY MATCH
    // =========================================================

    function permissionCategoryMatches(
        emp,
        selected_category
    ) {

        if (!selected_category) {
            return true;
        }

        const selected =
            String(selected_category)
                .trim()
                .toLowerCase();

        if (
            selected === "total" ||
            selected === "all"
        ) {
            return true;
        }

        const employee_category =
            String(
                emp.employee_category ||
                emp.category ||
                ""
            )
            .trim()
            .toLowerCase();

        const employment_type =
            String(
                emp.employment_type ||
                ""
            )
            .trim()
            .toLowerCase();

        const selected_normalized =
            selected;

        return (
            employee_category === selected_normalized ||
            employment_type === selected_normalized
        );

    }


    // =========================================================
    // PERMISSION SHIFT MATCH
    // =========================================================

    function permissionShiftMatches(
        emp,
        selected_shift
    ) {

        if (!selected_shift) {
            return true;
        }

        const selected =
            String(selected_shift)
                .trim()
                .toLowerCase();

        if (
            selected === "total" ||
            selected === "all"
        ) {
            return true;
        }

        const employee_shift =
            String(
                emp.shift ||
                emp.shift_type ||
                emp.shift_name ||
                ""
            )
            .trim()
            .toLowerCase();

        return employee_shift === selected;

    }


    // =========================================================
    // SHOW PERMISSION EMPLOYEES
    // =========================================================

    function show_permission_employees(
        selected_category = null,
        selected_shift = null
    ) {

        const from_date =
            $(wrapper).find("#perm-from-date").val();

        const to_date =
            $(wrapper).find("#perm-to-date").val();

        if (!from_date || !to_date) {

            frappe.msgprint(
                "Please select From Date and To Date"
            );

            return;

        }

        const category =
            selected_category
                ? String(selected_category).trim()
                : "";

        const shift =
            selected_shift
                ? String(selected_shift).trim()
                : "";

        const categoryProvided =
            category &&
            category.toLowerCase() !== "total" &&
            category.toLowerCase() !== "all";

        const shiftProvided =
            shift &&
            shift.toLowerCase() !== "total" &&
            shift.toLowerCase() !== "all";


        console.log(
            "Permission employee request:",
            {
                from_date: from_date,
                to_date: to_date,
                category: category,
                shift: shift
            }
        );


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_permission_employees",

            args: {

                from_date:
                    from_date,

                to_date:
                    to_date

            },

            callback: function(r) {

                let data =
                    Array.isArray(r.message)
                        ? r.message
                        : [];


                console.log(
                    "Permission records from backend BEFORE filtering:",
                    data
                );


                if (categoryProvided) {

                    data =
                        data.filter(function(emp) {

                            return permissionCategoryMatches(
                                emp,
                                category
                            );

                        });

                }


                if (shiftProvided) {

                    data =
                        data.filter(function(emp) {

                            return permissionShiftMatches(
                                emp,
                                shift
                            );

                        });

                }


                console.log(
                    "Permission records AFTER filtering:",
                    data
                );


                let title =
                    "Permission Employees";

                if (categoryProvided) {

                    title +=
                        " - " +
                        category;

                }

                if (shiftProvided) {

                    title +=
                        " - Shift " +
                        shift;

                }


                let html = `

                    <div
                        style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            margin-bottom:10px;
                        "
                    >

                        <div style="font-weight:600;">

                            Showing

                            <span style="color:#2563eb;">
                                ${data.length}
                            </span>

                            record(s)

                        </div>

                        <button
                            class="btn btn-success btn-sm"
                            id="perm-download-btn"
                        >
                            Download Excel
                        </button>

                    </div>

                    <div class="table-responsive">

                        <table
                            class="table table-bordered table-sm"
                            style="width:100%;"
                        >

                            <thead>

                                <tr>

                                    <th>Employee ID</th>
                                    <th>Name</th>
                                    <th>Shift</th>
                                    <th>Category</th>
                                    <th>Employment Type</th>
                                    <th>Session</th>
                                    <th>From Time</th>
                                    <th>To Time</th>
                                    <th>Status</th>
                                    <th>Approver</th>
                                    <th>Created On</th>

                                </tr>

                            </thead>

                            <tbody>

                `;


                if (!data.length) {

                    html += `

                        <tr>

                            <td
                                colspan="11"
                                style="
                                    text-align:center;
                                    padding:20px;
                                "
                            >
                                No records found
                            </td>

                        </tr>

                    `;

                }
                else {

                    data.forEach(function(emp) {

                        const employee_id =
                            emp.employee_id ||
                            emp.employee ||
                            emp.employee_code ||
                            "";


                        const employee_name =
                            emp.employee_name ||
                            emp.name ||
                            "";


                        const employee_shift =
                            emp.shift ||
                            emp.shift_type ||
                            emp.shift_name ||
                            "";


                        const employee_category =
                            emp.employee_category ||
                            emp.category ||
                            "";


                        const employment_type =
                            emp.employment_type ||
                            "";


                        let created = "";

                        if (emp.created_on) {

                            created =
                                frappe.datetime.str_to_user(
                                    emp.created_on
                                );

                        }
                        else if (emp.creation) {

                            created =
                                frappe.datetime.str_to_user(
                                    emp.creation
                                );

                        }


                        let status_color =
                            "secondary";

                        const status =
                            String(
                                emp.status ||
                                emp.workflow_state ||
                                ""
                            )
                            .trim()
                            .toLowerCase();

                        if (status === "approved") {

                            status_color =
                                "success";

                        }
                        else if (
                            status === "rejected"
                        ) {

                            status_color =
                                "danger";

                        }
                        else if (
                            status === "pending" ||
                            status === "incharge pending" ||
                            status === "superior pending"
                        ) {

                            status_color =
                                "warning";

                        }


                        html += `

                            <tr>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(employee_id)
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(employee_name)
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(employee_shift)
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(employee_category)
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(employment_type)
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(
                                            emp.session || ""
                                        )
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(
                                            emp.from_time || ""
                                        )
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(
                                            emp.to_time || ""
                                        )
                                    )}
                                </td>

                                <td>

                                    <span
                                        class="badge badge-${status_color}"
                                    >
                                        ${frappe.utils.escape_html(
                                            String(
                                                emp.status ||
                                                emp.workflow_state ||
                                                ""
                                            )
                                        )}
                                    </span>

                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(
                                            emp.approver || ""
                                        )
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(created)
                                    )}
                                </td>

                            </tr>

                        `;

                    });

                }


                html += `

                            </tbody>

                        </table>

                    </div>

                `;


                const d =
                    new frappe.ui.Dialog({

                        title:
                            title,

                        size:
                            "extra-large",

                        fields: [

                            {
                                fieldtype:
                                    "HTML",

                                fieldname:
                                    "table_html"
                            }

                        ]

                    });


                d.fields_dict
                    .table_html
                    .$wrapper
                    .html(html);


                d.fields_dict
                    .table_html
                    .$wrapper
                    .find("#perm-download-btn")
                    .on(
                        "click",
                        function() {

                            let download_url =
                                `/api/method/infac.infac.page.hr_dashboard_test.hr_dashboard_test.download_permission_excel?from_date=${encodeURIComponent(
                                    from_date
                                )}&to_date=${encodeURIComponent(
                                    to_date
                                )}`;


                            if (categoryProvided) {

                                download_url +=
                                    `&employee_category=${encodeURIComponent(
                                        category
                                    )}`;

                            }

                            if (shiftProvided) {

                                download_url +=
                                    `&shift=${encodeURIComponent(
                                        shift
                                    )}`;

                            }

                            window.open(
                                download_url
                            );

                        }
                    );


                d.show();

            },

            error: function(xhr) {

                console.error(
                    "Permission employee error:",
                    xhr
                );

                frappe.msgprint(
                    "Error loading permission employees."
                );

            }

        });

    }


    // =========================================================
    // PERMISSION COUNT CLICK
    // =========================================================

    $(wrapper).on(
        "click",
        ".permission-count-click",
        function(e) {

            e.preventDefault();
            e.stopPropagation();

            const category =
                $(this).attr(
                    "data-category"
                ) || null;

            const shift =
                $(this).attr(
                    "data-shift"
                ) || null;

            const clickedCount =
                Number(
                    $(this).attr(
                        "data-count"
                    )
                ) || 0;


            console.log(
                "Permission clicked:",
                {
                    category:
                        category,

                    shift:
                        shift,

                    expected_count:
                        clickedCount
                }
            );


            show_permission_employees(
                category,
                shift
            );

        }
    );


    // =========================================================
    // LEAVE SUMMARY
    // =========================================================

    function load_leave_app_summary() {

        const from_date =
            $(wrapper).find("#leave-from-date").val();

        const to_date =
            $(wrapper).find("#leave-to-date").val();

        if (!from_date || !to_date) {
            return;
        }

        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_leave_app_summary",

            args: {

                from_date: from_date,
                to_date: to_date

            },

            callback: function(r) {

                const response =
                    r.message || {};

                const data =
                    Array.isArray(response.details)
                        ? response.details
                        : [];

                render_leave_app_table(data);

                $(wrapper)
                    .find("#leave-card-count")
                    .text(data.length);

            }

        });

    }


    function render_leave_app_table(data) {

        if (!data.length) {

            $(wrapper)
                .find("#leave-detail-table")
                .html(`

                    <p style="color:red;">
                        No Leave Records Found
                    </p>

                `);

            return;

        }


        let html = `

            <table
                class="table table-bordered table-sm"
                style="table-layout:auto;width:100%;"
            >

                <thead>

                    <tr>

                        <th>Employee ID</th>
                        <th>Employee Name</th>
                        <th>From Date</th>
                        <th>To Date</th>
                        <th>Leave Type</th>
                        <th style="width:300px;">Reason</th>
                        <th>Status</th>
                        <th>Approver</th>

                    </tr>

                </thead>

                <tbody>

        `;


        data.forEach(row => {

            html += `

                <tr>

                    <td>
                        ${frappe.utils.escape_html(
                            String(row.employee || "")
                        )}
                    </td>

                    <td>
                        ${frappe.utils.escape_html(
                            String(row.employee_name || "")
                        )}
                    </td>

                    <td>
                        ${
                            row.from_date
                                ? frappe.datetime.str_to_user(
                                    row.from_date
                                )
                                : ""
                        }
                    </td>

                    <td>
                        ${
                            row.to_date
                                ? frappe.datetime.str_to_user(
                                    row.to_date
                                )
                                : ""
                        }
                    </td>

                    <td>
                        ${frappe.utils.escape_html(
                            String(row.leave_type || "")
                        )}
                    </td>

                    <td
                        style="
                            max-width:300px;
                            white-space:normal;
                            word-break:break-word;
                        "
                    >
                        ${frappe.utils.escape_html(
                            String(row.description || "")
                        )}
                    </td>

                    <td>
                        ${frappe.utils.escape_html(
                            String(row.workflow_state || "")
                        )}
                    </td>

                    <td>
                        ${frappe.utils.escape_html(
                            String(row.approver || "")
                        )}
                    </td>

                </tr>

            `;

        });


        html += `

                </tbody>

            </table>

        `;


        $(wrapper)
            .find("#leave-detail-table")
            .html(html);

    }


    $(wrapper).on(
        "click",
        "#leave-filter-btn",
        function() {

            load_leave_app_summary();

        }
    );


    // =========================================================
    // LEAVE DOWNLOAD
    // =========================================================

    $(wrapper).on(
        "click",
        "#leave-download-btn",
        function() {

            const from_date =
                $(wrapper).find("#leave-from-date").val();

            const to_date =
                $(wrapper).find("#leave-to-date").val();


            if (!from_date || !to_date) {

                frappe.msgprint(
                    "Please select From Date and To Date"
                );

                return;

            }


            frappe.call({

                method:
                    "infac.infac.page.hr_dashboard.hr_dashboard.get_leave_app_summary",

                args: {

                    from_date: from_date,
                    to_date: to_date

                },

                callback: function(r) {

                    const data =
                        (r.message || {}).details || [];


                    if (!data.length) {

                        frappe.msgprint(
                            "No data to download."
                        );

                        return;

                    }


                    const headers = [

                        "Employee ID",
                        "Employee Name",
                        "Leave Type",
                        "Session",
                        "From Date",
                        "To Date",
                        "Half Day",
                        "Total Leave Days",
                        "Status",
                        "Approver"

                    ];


                    const rows =
                        data.map(row => [

                            row.employee || "",
                            row.employee_name || "",
                            row.leave_type || "",
                            row.session || "",
                            row.from_date || "",
                            row.to_date || "",
                            row.half_day || "",
                            row.total_leave_days || "",
                            row.workflow_state || "",
                            row.approver || ""

                        ]);


                    const csv_content = [

                        headers,
                        ...rows

                    ]
                    .map(row =>

                        row
                            .map(val =>
                                `"${String(val).replace(
                                    /"/g,
                                    '""'
                                )}"`
                            )
                            .join(",")

                    )
                    .join("\n");


                    const blob =
                        new Blob(
                            [csv_content],
                            {
                                type:
                                    "text/csv;charset=utf-8;"
                            }
                        );


                    const url =
                        URL.createObjectURL(blob);


                    const a =
                        document.createElement("a");


                    a.href = url;

                    a.download =
                        `Leave_Summary_${from_date}_to_${to_date}.csv`;


                    document.body.appendChild(a);

                    a.click();

                    document.body.removeChild(a);

                    URL.revokeObjectURL(url);

                }

            });

        }
    );


    // =========================================================
    // LATE SUMMARY
    // =========================================================

    function loadLateSummary() {

        const from_date =
            $(wrapper).find("#late-from-date").val();

        const to_date =
            $(wrapper).find("#late-to-date").val();


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_late_summary",

            args: {

                from_date: from_date,
                to_date: to_date

            },

            callback: function(r) {

                const response =
                    r.message || {};

                const data =
                    Array.isArray(response.summary)
                        ? response.summary
                        : [];

                const total =
                    Number(response.total) || 0;

                let html = "";


                data.forEach(row => {

                    const shift =
                        row.description ||
                        row.shift ||
                        "";


                    html += `

                        <tr>

                            <td>
                                ${frappe.utils.escape_html(
                                    String(shift)
                                )}
                            </td>

                            ${lateCountCell(
                                row.staff,
                                "Staff",
                                shift
                            )}

                            ${lateCountCell(
                                row.worker,
                                "Worker",
                                shift
                            )}

                            ${lateCountCell(
                                row.naps,
                                "NAPS",
                                shift
                            )}

                            ${lateCountCell(
                                row.contract,
                                "Contract",
                                shift
                            )}

                            ${lateCountCell(
                                row.trainee,
                                "Trainee",
                                shift
                            )}

                        </tr>

                    `;

                });


                if (!data.length) {

                    html = `

                        <tr>

                            <td
                                colspan="6"
                                class="text-center"
                            >
                                No records found
                            </td>

                        </tr>

                    `;

                }


                $(wrapper)
                    .find("#late-summary-body")
                    .html(html);


                $(wrapper)
                    .find("#late-card-count")
                    .text(total);

            },

            error: function() {

                $(wrapper)
                    .find("#late-summary-body")
                    .html(`

                        <tr>

                            <td
                                colspan="6"
                                class="text-center text-danger"
                            >
                                Error loading late summary
                            </td>

                        </tr>

                    `);

            }

        });

    }


    // =========================================================
    // LATE COUNT CELL
    // =========================================================

    function lateCountCell(
        count,
        category,
        shift
    ) {

        const value =
            Number(count) || 0;


        if (!value) {

            return `

                <td class="text-center">
                    0
                </td>

            `;

        }


        const isTotalShift =
            String(shift)
                .trim()
                .toLowerCase() === "total";


        return `

            <td class="text-center">

                <span
                    class="
                        click-count
                        late-count-click
                        ${isTotalShift ? "total-click" : ""}
                    "
                    data-category="${frappe.utils.escape_html(
                        String(category)
                    )}"
                    data-shift="${frappe.utils.escape_html(
                        String(shift || "")
                    )}"
                >
                    ${value}
                </span>

            </td>

        `;

    }


    $(wrapper).on(
        "click",
        "#late-filter-btn",
        function() {

            loadLateSummary();

        }
    );


    // =========================================================
    // SHOW LATE EMPLOYEES
    // =========================================================

    function show_late_employees(
        selected_category = null,
        selected_shift = null
    ) {

        const from_date =
            $(wrapper).find("#late-from-date").val();

        const to_date =
            $(wrapper).find("#late-to-date").val();


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_late_employees",

            args: {

                from_date: from_date,
                to_date: to_date

            },

            callback: function(r) {

                let data =
                    Array.isArray(r.message)
                        ? r.message
                        : [];


                if (
                    selected_category &&
                    String(selected_category)
                        .trim()
                        .toLowerCase() !== "total"
                ) {

                    data =
                        data.filter(emp => {

                            const type =
                                String(
                                    emp.employee_category ||
                                    emp.employment_type ||
                                    emp.category ||
                                    ""
                                )
                                .trim()
                                .toLowerCase();


                            return type ===
                                String(selected_category)
                                    .trim()
                                    .toLowerCase();

                        });

                }


                if (
                    selected_shift &&
                    String(selected_shift)
                        .trim()
                        .toLowerCase() !== "all" &&
                    String(selected_shift)
                        .trim()
                        .toLowerCase() !== "total"
                ) {

                    data =
                        data.filter(emp => {

                            return String(
                                emp.shift || ""
                            )
                            .trim()
                            .toLowerCase()
                            ===
                            String(selected_shift)
                                .trim()
                                .toLowerCase();

                        });

                }


                let title =
                    "Late Employees";


                if (
                    selected_category &&
                    String(selected_category)
                        .trim()
                        .toLowerCase() !== "total"
                ) {

                    title +=
                        " - " +
                        selected_category;

                }


                if (
                    selected_shift &&
                    String(selected_shift)
                        .trim()
                        .toLowerCase() !== "all" &&
                    String(selected_shift)
                        .trim()
                        .toLowerCase() !== "total"
                ) {

                    title +=
                        " - Shift " +
                        selected_shift;

                }


                let html = `

                    <div
                        style="
                            text-align:right;
                            margin-bottom:10px;
                        "
                    >

                        <button
                            class="btn btn-primary btn-sm"
                            id="download-late-btn"
                        >
                            Download Excel
                        </button>

                    </div>

                    <table
                        class="table table-bordered table-sm"
                    >

                        <thead>

                            <tr>

                                <th>Employee</th>
                                <th>Name</th>
                                <th>Shift</th>
                                <th>Employment</th>
                                <th>Checkin Time</th>

                            </tr>

                        </thead>

                        <tbody>

                `;


                if (!data.length) {

                    html += `

                        <tr>

                            <td
                                colspan="5"
                                class="text-center"
                            >
                                No records found
                            </td>

                        </tr>

                    `;

                }
                else {

                    data.forEach(emp => {

                        const late_category =
                            emp.employee_category ||
                            emp.employment_type ||
                            emp.category ||
                            "";


                        html += `

                            <tr>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(emp.employee || "")
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(
                                            emp.employee_name || ""
                                        )
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(emp.shift || "")
                                    )}
                                </td>

                                <td>
                                    ${frappe.utils.escape_html(
                                        String(late_category)
                                    )}
                                </td>

                                <td>
                                    ${
                                        emp.time
                                            ? frappe.datetime.str_to_user(
                                                emp.time
                                            )
                                            : ""
                                    }
                                </td>

                            </tr>

                        `;

                    });

                }


                html += `

                        </tbody>

                    </table>

                `;


                const d =
                    new frappe.ui.Dialog({

                        title: title,

                        size: "extra-large",

                        fields: [

                            {
                                fieldtype: "HTML",
                                fieldname: "table_html"
                            }

                        ]

                    });


                d.fields_dict
                    .table_html
                    .$wrapper
                    .html(html);


                d.fields_dict
                    .table_html
                    .$wrapper
                    .find("#download-late-btn")
                    .on(
                        "click",
                        function() {

                            window.open(
                                `/api/method/infac.infac.page.hr_dashboard.hr_dashboard.download_late_excel?from_date=${encodeURIComponent(
                                    from_date
                                )}&to_date=${encodeURIComponent(
                                    to_date
                                )}`
                            );

                        }
                    );


                d.show();

            },

            error: function() {

                frappe.msgprint(
                    "Error loading late employees."
                );

            }

        });

    }


    // =========================================================
    // LATE COUNT CLICK
    // =========================================================

    $(wrapper).on(
        "click",
        ".late-count-click",
        function(e) {

            e.preventDefault();
            e.stopPropagation();


            const category =
                $(this).attr(
                    "data-category"
                );


            const shift =
                $(this).attr(
                    "data-shift"
                );


            show_late_employees(
                category,
                shift
            );

        }
    );


    // =========================================================
    // HEAD COUNT
    // =========================================================

    // function loadHeadCountDetails() {

    //     const selected_date =
    //         $(wrapper).find("#filter-date").val() ||
    //         frappe.datetime.get_today();


    //     const selected_shift =
    //         $(wrapper).find("#shift").val() ||
    //         "All";


    //     frappe.call({

    //         method:
    //             "infac.infac.page.hr_dashboard.hr_dashboard.get_headcount_summary",

    //         args: {

    //             attendance_date:
    //                 selected_date,

    //             shift:
    //                 selected_shift

    //         },

    //         callback: function(r) {

    //             if (!r.message) {
    //                 return;
    //             }


    //             const tbody =
    //                 $(wrapper)
    //                     .find("#dept-summary-body");


    //             tbody.empty();


    //             Object.keys(r.message)
    //                 .forEach(dept => {

    //                     const d =
    //                         r.message[dept];


    //                     const overall =
    //                         d.overall || {

    //                             avail: 0,
    //                             present: 0,
    //                             absent: 0

    //                         };


    //                     const absent_pct =
    //                         overall.avail
    //                             ? (
    //                                 (
    //                                     overall.absent /
    //                                     overall.avail
    //                                 ) * 100
    //                             ).toFixed(0)
    //                             : 0;


    //                     const tr =
    //                         document.createElement("tr");


    //                     tr.innerHTML = `

    //                         <td>
    //                             ${frappe.utils.escape_html(
    //                                 String(dept)
    //                             )}
    //                         </td>

    //                         <td>
    //                             ${overall.avail}
    //                         </td>

    //                         <td style="color:green">
    //                             ${overall.present}
    //                         </td>

    //                         <td style="color:red">
    //                             ${overall.absent}
    //                         </td>

    //                         <td>
    //                             <b>
    //                                 ${absent_pct}%
    //                             </b>
    //                         </td>

    //                         ${shiftCols(
    //                             d["1st Shift"]
    //                         )}

    //                         ${shiftCols(
    //                             d["General"]
    //                         )}

    //                         ${shiftCols(
    //                             d["2nd Shift"]
    //                         )}

    //                         ${shiftCols(
    //                             d["3rd Shift"]
    //                         )}

    //                     `;


    //                     tbody.append(tr);

    //                 });

    //         },

    //         error: function() {

    //             $(wrapper)
    //                 .find("#dept-summary-body")
    //                 .html(`

    //                     <tr>

    //                         <td
    //                             colspan="17"
    //                             class="text-center text-danger"
    //                         >
    //                             Error loading head count
    //                         </td>

    //                     </tr>

    //                 `);

    //         }

    //     });

    // }


    function loadHeadCountDetails() {

    const attendance_date =
        $(wrapper).find("#filter-date").val() ||
        frappe.datetime.get_today();

    const tbody = $(wrapper).find("#dept-summary-body");

    tbody.html(
        `<tr><td colspan="17" class="muted text-center p-3">Loading...</td></tr>`
    );

    frappe.call({
        method: "infac.infac.page.hr_dashboard.hr_dashboard.get_dept_summary",
        args: { attendance_date },
        callback: function (r) {

            const data = r.message || [];

            if (!data.length) {
                tbody.html(
                    `<tr><td colspan="17" class="text-center muted p-3">No data</td></tr>`
                );
                return;
            }

            let rows = "";

            data.forEach(d => {

                const absent_pct = (d.absent_pct ?? 0).toFixed(1) + "%";
                const bg = d.bg_color || "";

                rows += `
                    <tr style="background:${bg}">
                        <td>${frappe.utils.escape_html(d.department)}</td>

                        <td class="text-center">
                            <span class="click-plan text-primary"
                                  data-dept="${frappe.utils.escape_html(d.department)}"
                                  data-date="${attendance_date}">
                                ${d.available}
                            </span>
                        </td>

                        <td class="text-center">
                            <span class="click-present text-success"
                                  data-dept="${frappe.utils.escape_html(d.department)}"
                                  data-date="${attendance_date}">
                                ${d.present}
                            </span>
                        </td>

                        <td class="text-center text-danger">${d.absent}</td>
                        <td class="text-center"><b>${absent_pct}</b></td>

                        ${renderShiftCols(d["1st Shift"])}
                        ${renderShiftCols(d["General"])}
                        ${renderShiftCols(d["2nd Shift"])}
                        ${renderShiftCols(d["3rd Shift"])}
                    </tr>
                `;
            });

            tbody.html(rows);
        },

        error: function() {
            tbody.html(
                `<tr><td colspan="17" class="text-center text-danger">Error loading head count</td></tr>`
            );
        }
    });
}


function renderShiftCols(shift) {
    if (!shift) {
        return `<td class="text-center">0</td><td class="text-center">0</td><td class="text-center">0</td>`;
    }
    return `
        <td class="text-center text-primary">${shift.plan}</td>
        <td class="text-center text-success">${shift.present}</td>
        <td class="text-center text-danger">${shift.absent}</td>
    `;
}

    // function shiftCols(s) {

    //     s =
    //         s || {

    //             plan: 0,
    //             present: 0,
    //             absent: 0

    //         };


    //     return `

    //         <td>
    //             ${s.plan}
    //         </td>

    //         <td style="color:green">
    //             ${s.present}
    //         </td>

    //         <td style="color:red">
    //             ${s.absent}
    //         </td>

    //     `;

    // }


    // =========================================================
    // CONTRACTOR SUMMARY
    // =========================================================

    function loadContractorSummary(date) {

        const selected_shift =
            $(wrapper).find("#shift").val() ||
            "All";


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_contractor_summary",

            args: {

                attendance_date: date,

                shift: selected_shift

            },

            callback: function(r) {

                if (!Array.isArray(r.message)) {
                    return;
                }


                const tbody =
                    $(wrapper)
                        .find("#late-reason-body");


                tbody.empty();


                r.message.forEach(row => {

                    const rowStyle =
                        row.contractor === "Total"
                            ? 'style="font-weight:bold;background:#f1f1f1;"'
                            : "";


                    tbody.append(`

                        <tr ${rowStyle}>

                            <td style="text-align:left;">

                                ${frappe.utils.escape_html(
                                    String(
                                        row.contractor || "-"
                                    )
                                )}

                            </td>

                            <td style="text-align:center;">

                                ${row.enrolled || 0}

                            </td>

                            <td style="text-align:center;">

                                ${row.present || 0}

                            </td>

                            <td style="text-align:center;">

                                ${row.absent || 0}

                            </td>

                        </tr>

                    `);

                });

            },

            error: function() {

                $(wrapper)
                    .find("#late-reason-body")
                    .html(`

                        <tr>

                            <td
                                colspan="4"
                                class="text-center text-danger"
                            >
                                Error loading contractor summary
                            </td>

                        </tr>

                    `);

            }

        });

    }


    // =========================================================
    // DEPARTMENT LINE SUMMARY
    // =========================================================

    function loadDeptLineSummary() {

        const attendance_date =
            $(wrapper).find("#filter-date").val();


        const shift =
            $(wrapper).find("#shift").val() ||
            "All";


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_dept_line_summary",

            args: {

                attendance_date:
                    attendance_date,

                shift:
                    shift

            },

            callback: function(r) {

                const data =
                    Array.isArray(r.message)
                        ? r.message
                        : [];


                const tbody =
                    $(wrapper)
                        .find(
                            "#dept_line_summary tbody"
                        );


                tbody.empty();


                if (!data.length) {

                    tbody.append(`

                        <tr>

                            <td
                                colspan="5"
                                class="text-center text-muted"
                            >
                                No data
                            </td>

                        </tr>

                    `);

                    return;

                }


                data.forEach(row => {

                    let rowStyle = "";


                    if (
                        row.department_line &&
                        String(row.department_line)
                            .trim()
                            .toLowerCase() === "total"
                    ) {

                        rowStyle =
                            "font-weight:bold;background-color:#e3f2fd;";

                    }
                    else if (row.bg_color) {

                        rowStyle =
                            `background-color:${row.bg_color};`;

                    }


                    tbody.append(`

                        <tr style="${rowStyle}">

                            <td>

                                ${frappe.utils.escape_html(
                                    String(
                                        row.department_line || ""
                                    )
                                )}

                            </td>

                            <td class="text-center">
                                ${row.available || 0}
                            </td>

                            <td class="text-center">
                                ${row.present || 0}
                            </td>

                            <td class="text-center">
                                ${row.absent || 0}
                            </td>

                            <td class="text-center">
                                ${row.absent_pct || 0}%
                            </td>

                        </tr>

                    `);

                });

            },

            error: function() {

                $(wrapper)
                    .find("#dept_line_summary tbody")
                    .html(`

                        <tr>

                            <td
                                colspan="5"
                                class="text-center text-danger"
                            >
                                Error loading department line summary
                            </td>

                        </tr>

                    `);

            }

        });

    }


    // =========================================================
    // DEPARTMENT LINE DOWNLOAD
    // =========================================================

    $(wrapper).on(
        "click",
        "#download-dept-line",
        function() {

            const table =
                $(wrapper)
                    .find(
                        "#dept_line_summary"
                    )[0];


            if (!table) {

                frappe.msgprint(
                    "No table found to download."
                );

                return;

            }


            if (
                typeof XLSX === "undefined"
            ) {

                frappe.msgprint(
                    "Excel library is not loaded."
                );

                return;

            }


            const wb =
                XLSX.utils.table_to_book(
                    table,
                    {
                        sheet:
                            "Dept Line Summary"
                    }
                );


            XLSX.writeFile(
                wb,
                "Department_Line_Summary.xlsx"
            );

        }
    );


    // =========================================================
    // APPLY MAIN FILTER
    // =========================================================

    $(wrapper).on(
        "click",
        "#apply-filter",
        function() {

            const date =
                $(wrapper)
                    .find("#filter-date")
                    .val();


            loadHeadCountDetails();

            loadLateSummary();

            load_permission_summary();

            load_leave_app_summary();

            loadContractorSummary(
                date
            );

            loadDeptLineSummary();

        }
    );


    // =========================================================
    // DATE CHANGE
    // =========================================================

    $(wrapper).on(
        "change",
        "#filter-date",
        function() {

            loadHeadCountDetails();

            loadContractorSummary(
                $(this).val()
            );

            loadDeptLineSummary();

        }
    );


    // =========================================================
    // SHIFT CHANGE
    // =========================================================

    $(wrapper).on(
        "change",
        "#shift",
        function() {

            loadHeadCountDetails();

            loadContractorSummary(
                $(wrapper)
                    .find("#filter-date")
                    .val()
            );

            loadDeptLineSummary();

        }
    );


    // =========================================================
    // DEPARTMENT PRESENT CLICK
    // =========================================================

    $(wrapper).on(
        "click",
        ".click-present",
        function() {

            const dept =
                String(
                    $(this).data("dept")
                ).trim();


            const date =
                $(this).data("date");


            frappe.set_route(
                "Report",
                "Employee Checkin",
                {

                    log_type:
                        "IN",

                    department:
                        dept,

                    time: [
                        "between",
                        [
                            date + " 00:00:00",
                            date + " 23:59:59"
                        ]
                    ]

                }
            );

        }
    );


    // =========================================================
    // DEPARTMENT PLAN CLICK
    // =========================================================

    $(wrapper).on(
        "click",
        ".click-plan",
        function() {

            const dept =
                String(
                    $(this).data("dept")
                ).trim();


            const date =
                $(this).data("date");


            frappe.set_route(
                "Report",
                "Shift Assignment",
                {

                    department:
                        dept,

                    start_date: [
                        "<=",
                        date
                    ],

                    end_date: [
                        ">=",
                        date
                    ],

                    docstatus:
                        1

                }
            );

        }
    );


    // =========================================================
    // WEEKLY CHART
    // =========================================================

    const chart_script =
        document.createElement("script");


    chart_script.src =
        "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js";


    chart_script.onload = function() {

        const dl =
            document.createElement("script");


        dl.src =
            "https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2";


        dl.onload = function() {

            let chartInstance = null;


            // =============================================
            // FETCH WEEKLY ATTENDANCE
            // =============================================

            function fetchWeeklyAttendance(
                from_date,
                to_date
            ) {

                frappe.call({

                    method:
                        "infac.infac.page.hr_dashboard.hr_dashboard.get_weekly_attendance",

                    args: {

                        from_date:
                            from_date,

                        to_date:
                            to_date

                    },

                    callback: function(r) {

                        if (!r.message) {
                            return;
                        }


                        const data =
                            Array.isArray(r.message)
                                ? r.message
                                : [];


                        const labels =
                            data.map(
                                d => d.date
                            );


                        const percent =
                            data.map(
                                d =>
                                    Number(
                                        d.percent
                                    ) || 0
                            );


                        let rows = "";


                        data.forEach(d => {

                            rows += `

                                <tr>

                                    <td
                                        style="
                                            text-align:center;
                                            background:#f5f5f5;
                                        "
                                    >
                                        ${frappe.utils.escape_html(
                                            String(d.date || "")
                                        )}
                                    </td>

                                    <td
                                        style="
                                            text-align:center;
                                        "
                                    >
                                        ${d.plan || 0}
                                    </td>

                                    <td
                                        style="
                                            text-align:center;
                                        "
                                    >
                                        ${d.actual || 0}
                                    </td>

                                    <td
                                        style="
                                            text-align:center;
                                        "
                                    >
                                        ${d.gap || 0}
                                    </td>

                                    <td
                                        style="
                                            text-align:center;
                                        "
                                    >
                                        ${d.percent || 0}%
                                    </td>

                                </tr>

                            `;

                        });


                        if (!data.length) {

                            rows = `

                                <tr>

                                    <td
                                        colspan="5"
                                        class="text-center"
                                    >
                                        No records found
                                    </td>

                                </tr>

                            `;

                        }


                        $(wrapper)
                            .find(
                                "#weekly-attendance-body"
                            )
                            .html(rows);


                        const canvas =
                            $(wrapper)
                                .find(
                                    "#weeklyAttendanceChart"
                                )[0];


                        if (!canvas) {
                            return;
                        }


                        if (
                            typeof Chart === "undefined"
                        ) {

                            console.error(
                                "Chart.js is not loaded."
                            );

                            return;

                        }


                        const ctx =
                            canvas.getContext("2d");


                        if (chartInstance) {

                            chartInstance.destroy();

                            chartInstance = null;

                        }


                        chartInstance =
                            new Chart(
                                ctx,
                                {

                                    type: "line",

                                    data: {

                                        labels:
                                            labels,

                                        datasets: [

                                            {

                                                label:
                                                    "% Attendance",

                                                data:
                                                    percent,

                                                borderWidth:
                                                    2,

                                                tension:
                                                    0.3,

                                                pointRadius:
                                                    4

                                            }

                                        ]

                                    },

                                    options: {

                                        responsive:
                                            true,

                                        maintainAspectRatio:
                                            true,

                                        plugins: {

                                            datalabels: {

                                                display:
                                                    true,

                                                align:
                                                    "top",

                                                anchor:
                                                    "end",

                                                offset:
                                                    4,

                                                clip:
                                                    false,

                                                clamp:
                                                    true,

                                                font: {

                                                    weight:
                                                        "bold",

                                                    size:
                                                        11

                                                },

                                                formatter:
                                                    function(value) {

                                                        return value +
                                                            "%";

                                                    }

                                            }

                                        },

                                        scales: {

                                            y: {

                                                beginAtZero:
                                                    true,

                                                title: {

                                                    display:
                                                        true,

                                                    text:
                                                        "Percentage (%)"

                                                }

                                            },

                                            x: {

                                                title: {

                                                    display:
                                                        true,

                                                    text:
                                                        "Date"

                                                }

                                            }

                                        }

                                    },

                                    plugins: [

                                        ChartDataLabels

                                    ]

                                }
                            );

                    },

                    error: function() {

                        $(wrapper)
                            .find(
                                "#weekly-attendance-body"
                            )
                            .html(`

                                <tr>

                                    <td
                                        colspan="5"
                                        class="text-center text-danger"
                                    >
                                        Error loading weekly attendance
                                    </td>

                                </tr>

                            `);

                    }

                });

            }


            // =============================================
            // DEFAULT WEEK DATES
            // =============================================

            function setDefaultWeekDates() {

                const todayDate =
                    new Date();


                const day =
                    todayDate.getDay();


                const diffToMonday =
                    day === 0
                        ? -6
                        : 1 - day;


                const monday =
                    new Date(
                        todayDate
                    );


                monday.setDate(
                    todayDate.getDate() +
                    diffToMonday
                );


                const saturday =
                    new Date(
                        monday
                    );


                saturday.setDate(
                    monday.getDate() + 5
                );


                const formatDate =
                    date => {

                        const year =
                            date.getFullYear();


                        const month =
                            String(
                                date.getMonth() + 1
                            )
                            .padStart(2, "0");


                        const day =
                            String(
                                date.getDate()
                            )
                            .padStart(2, "0");


                        return `${year}-${month}-${day}`;

                    };


                $(wrapper)
                    .find("#from-date")
                    .val(
                        formatDate(monday)
                    );


                $(wrapper)
                    .find("#to-date")
                    .val(
                        formatDate(saturday)
                    );

            }


            setDefaultWeekDates();


            // =============================================
            // WEEKLY FILTER
            // =============================================

            $(wrapper).on(
                "click",
                "#apply-weekly-filter",
                function() {

                    const from_date =
                        $(wrapper)
                            .find("#from-date")
                            .val();


                    const to_date =
                        $(wrapper)
                            .find("#to-date")
                            .val();


                    if (
                        !from_date ||
                        !to_date
                    ) {

                        frappe.msgprint(
                            "Please select both From and To dates"
                        );

                        return;

                    }


                    if (from_date > to_date) {

                        frappe.msgprint(
                            "From Date cannot be greater than To Date"
                        );

                        return;

                    }


                    fetchWeeklyAttendance(
                        from_date,
                        to_date
                    );

                }
            );


            // =============================================
            // INITIAL WEEKLY LOAD
            // =============================================

            const from_date =
                $(wrapper)
                    .find("#from-date")
                    .val();


            const to_date =
                $(wrapper)
                    .find("#to-date")
                    .val();


            if (
                from_date &&
                to_date
            ) {

                fetchWeeklyAttendance(
                    from_date,
                    to_date
                );

            }

        };


        document.head.appendChild(dl);

    };


    document.head.appendChild(chart_script);


    // =========================================================
    // INITIAL LOAD
    // =========================================================

    loadHeadCountDetails();

    loadLateSummary();

    load_permission_summary();

    load_leave_app_summary();

    loadContractorSummary(
        today
    );

    loadTxnCalendar();

    loadDeptLineSummary();

};