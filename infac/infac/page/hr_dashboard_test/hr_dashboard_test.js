// frappe.pages['hr-dashboard-test'].on_page_load = function (wrapper) {

//     const page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'HR Dashboard Test',
//         single_column: true
//     });

//     frappe.breadcrumbs.add('infac');



//     // Styles
//     const style = document.createElement('style');
//     style.innerHTML = `
//         .dashboard-wrapper {
//             padding: 16px;
//             min-height: calc(100vh - 120px);
//             background: linear-gradient(180deg, #f7fafc 0%, #eef2f7 100%);
//         }
//         .page-header {
// 			display: grid;
// 			grid-template-columns: 1fr auto;  /* left = center title, right = filters */
// 			align-items: center;
// 			margin-bottom: 20px;
// 		}
// 		.dashboard-box1 {
// 			display: block; /* flex illa */
// 		}
// 		.page-title-center {
// 			text-align: center;
// 			grid-column: 1 / -1;   /* span full row */
// 			margin-bottom: 8px;
// 		}

// 		.page-title-center h2 {
// 			font-size: 24px;
// 			font-weight: 700;
// 			margin: 0;
// 		}
//         .page-header h2 {
//             font-size: 24px;
//             font-weight: 700;
//             margin: 0;
//         }
//         .filters {
//             display: flex;
//             gap: 8px;
//             align-items: center;
//         }
//         .hr-layout {
//             display: grid;
//             grid-template-columns: 1fr 1fr 1fr;  /* half-half layout */
//             gap: 16px;
			
//         }
//         .hr-card {
//             background: #ffffff;
//             border-radius: 16px;
//             box-shadow: 0 10px 24px rgba(0,0,0,0.06);
//             padding: 16px;
//             border: 1px solid #101111ff;
//             height: fit-content;
//         }
//         .hr-card h3 {
//             font-size: 16px;
//             font-weight: 600;
//             margin: 0 0 12px 0;
//         }
//         .styled-table {
// 			width: 100%;
// 			border-collapse: collapse; /* no double borders */
// 			margin-top: 10px;
// 			font-size: 14px;
// 			text-align: center;  /* default center for all */
// 			}
//         .hr-table {
//             width: 100%;
//             border-collapse: collapse;
//             margin-top: 10px;
//             font-size: 14px;
//             text-align: center;
//             border: 1px solid #ccc;   /* full outer border */
//         }

//         .hr-table th,
//         .hr-table td {
//             border: 1px solid #ccc;   /* cell borders */
//             padding: 10px 12px;
//         }

//         .hr-table thead th {
//             background: #f9fafb;
//             font-size: 13px;
//             font-weight: 600;
//             color: #111827;
//             text-align: left;
//         }

//         /* ✅ force bottom border for last row */
//         .hr-table tr:last-child td {
//             border-bottom: 1px solid #ccc;
//         }

//         .leave-circle {
//     width: 150px;
//     height: 150px;
//     border-radius: 50%;
//     display: flex;
//     align-items: center;
//     justify-content: center;
//     position: relative;
//     margin: 0 auto;
// }

// .leave-circle .percent-text {
//     position: absolute;
//     text-align: center;
//     font-weight: bold;
//     font-size: 14px;
// }

// .leave-circle .approved-text {
//     color: #1c1e0eff;
// }

// .leave-circle .unapproved-text {
//     color: #dc2626;
// }

// #matrix-table th:first-child,
// #matrix-table td:first-child {
//     background-color: #d0e7ff;  /* light blue */
// }


// 		.leave-label {
// 			background: rgba(255, 255, 255, 0.6);
// 			padding: 8px;
// 			border-radius: 10px;
// 		}		
//         .badge-green { color: #16a34a; background: #ecfdf5; }
//         .badge-red { color: #dc2626; background: #fef2f2; }
//         .badge-blue { color: #2563eb; background: #eff6ff; }
//         .center { text-align: center; }
//         .muted { color: #64748b; }
//     `;
//     document.head.appendChild(style);

//     const xlsxScript = document.createElement("script");
//     xlsxScript.src = "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js";
//     document.head.appendChild(xlsxScript);

//     // HTML
//     $(wrapper).html(`
//     <div class="dashboard-wrapper">
//         <div class="page-header">
//             <div class="page-title-center">
//                 <h2>HR Dashboard</h2>
//             </div>
//             <div style="display: flex; align-items: center; gap: 10px; justify-content: center; margin-bottom: 15px;">
//                 <input type="date" id="filter-date" class="form-control" style="width: 200px; font-size: 14px;">
//                 <select id="shift" class="form-control" style="width: 200px; font-size: 14px;">
//                     <option value="All">All Shift</option>
//     <option value="A">A</option>
//     <option value="B">B</option>
//     <option value="C">C</option>
//     <option value="G">G</option>
//                 </select>
//                 <button id="apply-filter" class="btn btn-primary">Apply</button>
//             </div>
//         </div>
//         <div class="hr-layout" style="display:flex; gap:20px; flex-wrap:wrap;">
//             <div class="middle-column" style="flex:1; display:flex; flex-direction:column; gap:20px;">
//                 <!-- Left card -->
//                 <div class="hr-card" style="width:100%;">
//                     <h3>Head Count Details</h3>
//                     <div class="table-responsive" style="height:950px;">
//                         <table class="hr-table" style="width:100%;">
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

//                                     <th>Plan</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>

//                                     <th>Plan</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>

//                                     <th>Plan</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>

//                                     <th>Plan</th>
//                                     <th>Present</th>
//                                     <th>Absent</th>
//                                 </tr>
//                             </thead>
//                             <tbody id="dept-summary-body"></tbody>
//                         </table>

//                     </div>
//                 </div>    
//                 <div class="hr-card" style="width:100%;">
//                     <div class="attendance-summary-section" style="margin-top:20px;min-height:390px;">
//                             <h3 style="text-align:left;">Weekly Attendance Summary Graph</h3>

//                             <!-- Filter -->
//                             <div style="display:flex; justify-content:center; gap:10px; margin-bottom:15px;">
//                                 <input type="date" id="from-date" class="form-control" style="width:180px;">
//                                 <input type="date" id="to-date" class="form-control" style="width:180px;">
//                                 <button id="apply-weekly-filter" class="btn btn-primary">Apply</button>
//                             </div>

//                             <canvas id="weeklyAttendanceChart" height="200"></canvas>
//                     </div>
//                 </div>  

//             </div>
//             <!-- Middle Column -->
//             <div class="middle-column" style="flex:1; display:flex; flex-direction:column; gap:20px;">

//                 <!-- Contractor Wise Attendance -->
//                 <div class="hr-card" style="width:100%;">
//                     <h3>Contractor Wise Attendance</h3>
//                     <div class="table-responsive" style="max-height:600px; overflow:auto;">
//                         <table class="hr-table" style="width:100%; border-collapse:collapse;">
//                             <thead>
//                                 <tr>
//                                     <th style="width:40%; text-align:center;">Contractor Name</th>
//                                     <th style="width:20%; text-align:center;">Available</th>
//                                     <th style="width:20%; text-align:center;">Present</th>
//                                     <th style="width:20%; text-align:center;">Absent</th>
//                                 </tr>
//                             </thead>
//                             <tbody id="late-reason-body">
//                                 <tr><td colspan="4" style="text-align:center;padding:16px;">Loading…</td></tr>
//                             </tbody>
//                         </table>
//                     </div>
//                 </div>

// <div class="hr-card" style="width:100%;">
//     <h3>Late Entry Details</h3>

//     <div class="table-responsive">
//         <table class="hr-table" id="late-summary-table">

//             <thead>
//                 <tr>
//                     <th>Shift/Category</th>
//                     <th>Staff</th>
//                     <th>Worker</th>
//                     <th>NAPS</th>
//                     <th>Contract</th>
//                     <th>Trainee</th>
//                 </tr>
//             </thead>

//             <tbody id="late-summary-body">
//                 <tr>
//                     <td colspan="6" style="text-align:center;padding:16px;">
//                         Loading...
//                     </td>
//                 </tr>
//             </tbody>

//         </table>
//     </div>
// </div>  
//               <div class="hr-card" style="width:100%;">
//                     <div class="table-responsive" style="margin-top:20px;max-height:420px; overflow-y:auto;">
//                         <h3 style="text-align:left;">Weekly Attendance Summary Table</h3>
//                         <br>
//                         <table class="hr-table" style="width:100%;border-collapse:collapse;">
//                             <thead>
//                                 <tr style="background-color:#f5f5f5;">
//                                     <th style="text-align:center;">Date</th>
//                                     <th style="text-align:center;">Plan</th>
//                                     <th style="text-align:center;">Actual</th>
//                                     <th style="text-align:center;">Gap</th>
//                                     <th style="text-align:center;">%</th>
//                                 </tr>
//                             </thead>
//                             <tbody id="weekly-attendance-body">
//                                 <tr>
//                                     <td colspan="5" style="text-align:center; padding:16px;">Loading...</td>
//                                 </tr>
//                             </tbody>
//                         </table>
//                         <br>
//                     </div>
//                 </div>

//             </div>

//             <!-- Right Column -->
//             <div class="right-column" style="flex:0.4; display:flex; flex-direction:column; gap:20px;">

//                 <!-- Approved Leave -->
//                 <div class="hr-card" style="width:100%;">
//                     <h3>Approved Leave Summary</h3>
//                     <div class="leave-circle">
//                         <div class="percent-text">
//                             <div class="approved-text">0%</div>
//                             <div class="unapproved-text">0%</div>
//                         </div>
//                     </div>
//                     <div class="leave-label"></div>
//                  </div>

//                 <!-- Category Wise Absent -->
//                 <div class="hr-card" style="width:100%;">
//                     <h3>Category Wise Absent Count</h3>
//                     <div style="display:flex; justify-content:center; align-items:center;">
//                         <div class="headcount-circle" 
//                             style="width:150px; height:150px; border-radius:50%; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
//                         </div>
//                     </div>
//                     <div class="headcount-label" style="font-size:12px; font-weight:500; margin-top:15px; text-align:center;"></div>
//                 </div>

//                 <!-- Late Count -->
//                 <div class="hr-card" style="width:100%;">
//                     <h3 style="text-align:center;">Late Count Chart</h3>
//                     <div class="late-circle" 
//                         style="width:150px; height:150px; border-radius:50%; margin:10px auto; box-shadow:0 2px 6px rgba(0,0,0,0.2);">
//                     </div>
//                     <div class="late-label" style="text-align:center; font-size:14px; font-weight:500;"></div>  
//                 </div>

//             </div>


// <div id="dept_line_summary_container" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 8px;">
//     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
//         <h5 style="margin: 0;">Department Line Summary</h5>
//         <button class="btn btn-sm btn-primary" onclick="downloadDeptLineSummary()">
//             <i class="fa fa-download"></i> Download
//         </button>
//     </div>

//     <table id="dept_line_summary" class="table table-bordered table-sm">
//         <thead>
//             <tr>
//                 <th>Department Line</th>
//                 <th class="text-end">Available</th>
//                 <th class="text-end">Present</th>
//                 <th class="text-end">Absent</th>
//                 <th class="text-end">Absent %</th>
//             </tr>
//         </thead>
//         <tbody></tbody>
//     </table>
// </div>


//     </div>
// `);


//     // set default date = today
//     const $date = $(wrapper).find('#filter-date');
//     $date.val(frappe.datetime.get_today());

//     // const loadData = () => {
//     //     const attendance_date = document.getElementById("filter-date").value || frappe.datetime.get_today();
//     //     const shift = document.getElementById("shift").value || "All";
//     //     const $tbody = $(wrapper).find('#dept-summary-body');
//     //     $tbody.html(`<tr><td colspan="5" class="muted" style="text-align:center;padding:16px;">Loading…</td></tr>`);

//     //     frappe.call({
//     //         method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_dept_summary",
//     //         args: { attendance_date, shift },
//     //         callback: function(r) {
//     //             const data = r.message || [];
//     //             if (!data.length) {
//     //                 $tbody.html(`<tr><td colspan="5" class="muted" style="text-align:center;padding:16px;">No data</td></tr>`);
//     //                 return;
//     //             }
//     //             const rows = data.map(d => {
//     //                 const absent_pct = (d.absent_pct ?? 0).toFixed(1) + '%';
//     //                 const is_total = d.department === "Total";
//     //                 let bg_style = "";
//     //                 if (d.bg_color) {
//     //                     bg_style = `background-color:${d.bg_color};font-weight:bold;`;
//     //                 } else if (d.department && d.department.toLowerCase().includes("total")) {
//     //                     bg_style = "background-color:#f1f1f1;font-weight:bold;";
//     //                 }

//     //                 return `
//     //                     <tr ${is_total ? 'style="font-weight:bold;background:#f1f1f1;"' : ''}>
//     //                         <td style="text-align: left;">${frappe.utils.escape_html(d.department || "-")}</td>
//     //                         <td class="center"><span class="badge badge-blue">${d.available || 0}</span></td>
//     //                         <td class="center"><span class="badge badge-green">${d.present || 0}</span></td>
//     //                         <td class="center"><span class="badge badge-red">${d.absent || 0}</span></td>
//     //                         <td class="center"><strong>${absent_pct}</strong></td>
//     //                     </tr>
//     //                 `;
//     //             }).join('');
//     //             $tbody.html(rows);
//     //         }
//     //     });
//     // };




//     const loadData = () => {
//         const attendance_date =
//             document.getElementById("filter-date")?.value ||
//             frappe.datetime.get_today();

//         const $tbody = $(wrapper).find("#dept-summary-body");

//         $tbody.html(`
//         <tr>
//             <td colspan="20" class="muted text-center p-3">
//                 Loading...
//             </td>
//         </tr>
//     `);

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_dept_summary",
//             args: { attendance_date },
//             callback: (r) => {
//                 const data = r.message || [];

//                 if (!data.length) {
//                     $tbody.html(`
//                     <tr>
//                         <td colspan="20" class="text-center muted p-3">
//                             No data
//                         </td>
//                     </tr>
//                 `);
//                     return;
//                 }

//                 let rows = "";
//                 let grand = {
//                     available: 0,
//                     present: 0,
//                     absent: 0,
//                     shifts: {
//                         "1st Shift": { plan: 0, present: 0, absent: 0 },
//                         "General": { plan: 0, present: 0, absent: 0 },
//                         "2nd Shift": { plan: 0, present: 0, absent: 0 },
//                         "3rd Shift": { plan: 0, present: 0, absent: 0 }
//                     }
//                 };

//                 data.forEach(d => {
//                     const absent_pct = (d.absent_pct ?? 0).toFixed(1) + "%";

//                     rows += `
//                     <tr>
//                         <td>${frappe.utils.escape_html(d.department)}</td>

//                         <td class="text-center text-primary">${d.available}</td>
//                         <td class="text-center text-success">${d.present}</td>
//                         <td class="text-center text-danger">${d.absent}</td>
//                         <td class="text-center"><b>${absent_pct}</b></td>

//                         ${renderShiftCols(d["1st Shift"])}
//                         ${renderShiftCols(d["General"])}
//                         ${renderShiftCols(d["2nd Shift"])}
//                         ${renderShiftCols(d["3rd Shift"])}
//                     </tr>
//                 `;

//                     // Grand total calc
//                     grand.available += d.available;
//                     grand.present += d.present;
//                     grand.absent += d.absent;

//                     ["1st Shift", "General", "2nd Shift", "3rd Shift"].forEach(s => {
//                         grand.shifts[s].plan += d[s]?.plan || 0;
//                         grand.shifts[s].present += d[s]?.present || 0;
//                         grand.shifts[s].absent += d[s]?.absent || 0;
//                     });
//                 });

//                 const grand_pct = grand.available
//                     ? ((grand.absent / grand.available) * 100).toFixed(1)
//                     : "0.0";

//                 rows += `
//                 <tr style="background:#FFF3CD;font-weight:bold;">
//                     <td>GRAND TOTAL</td>

//                     <td class="text-center">${grand.available}</td>
//                     <td class="text-center">${grand.present}</td>
//                     <td class="text-center">${grand.absent}</td>
//                     <td class="text-center">${grand_pct}%</td>

//                     ${renderShiftCols(grand.shifts["1st Shift"])}
//                     ${renderShiftCols(grand.shifts["General"])}
//                     ${renderShiftCols(grand.shifts["2nd Shift"])}
//                     ${renderShiftCols(grand.shifts["3rd Shift"])}
//                 </tr>
//             `;

//                 $tbody.html(rows);
//             }
//         });
//     };

//     function renderShiftCols(shift) {
//         if (!shift) {
//             return `
//             <td class="text-center">0</td>
//             <td class="text-center">0</td>
//             <td class="text-center">0</td>
//         `;
//         }

//         return `
//         <td class="text-center text-primary">${shift.plan}</td>
//         <td class="text-center text-success">${shift.present}</td>
//         <td class="text-center text-danger">${shift.absent}</td>
//     `;
//     }

//     //     const loadData = () => {
//     //     const attendance_date = document.getElementById("filter-date").value || frappe.datetime.get_today();
//     //     const shift = document.getElementById("shift").value || "All";
//     //     const $tbody = $(wrapper).find('#dept-summary-body');
//     //     $tbody.html(`<tr><td colspan="5" class="muted" style="text-align:center;padding:16px;">Loading…</td></tr>`);

//     //     frappe.call({
//     //         method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_dept_summary",
//     //         args: { attendance_date, shift },
//     //         callback: function(r) {
//     //             const data = r.message || [];
//     //             if (!data.length) {
//     //                 $tbody.html(`<tr><td colspan="5" class="muted" style="text-align:center;padding:16px;">No data</td></tr>`);
//     //                 return;
//     //             }

//     //             const rows = data.map(d => {
//     //                 const absent_pct = (d.absent_pct ?? 0).toFixed(1) + '%';
//     //                 const bg_style = d.bg_color ? `background-color:${d.bg_color};font-weight:bold;` : "";

//     //                 return `
//     //                     <tr style="${bg_style}">
//     //                         <td style="text-align:left;">${frappe.utils.escape_html(d.department || "-")}</td>
//     //                         <td class="center"><span class="badge badge-blue">${d.available || 0}</span></td>
//     //                         <td class="center"><span class="badge badge-green">${d.present || 0}</span></td>
//     //                         <td class="center"><span class="badge badge-red">${d.absent || 0}</span></td>
//     //                         <td class="center"><strong>${absent_pct}</strong></td>
//     //                     </tr>
//     //                 `;
//     //             }).join('');

//     //             $tbody.html(rows);
//     //         }
//     //     });
//     // };


//     window.loadDeptLineSummary = function () {
//         const attendance_date = $date.val();
//         const shift = $("#shift").val() || "All";

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_dept_line_summary",
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
//                     let rowStyle = "";

//                     if (row.department_line && row.department_line.trim().toLowerCase() === "total") {
//                         // Highlight Total row
//                         rowStyle = `font-weight:bold; background-color:#e3f2fd;`; // light blue background + bold
//                     } else if (row.bg_color) {
//                         rowStyle = `background-color:${row.bg_color};`;
//                     }

//                     tbody.append(`
//                     <tr style="${rowStyle}">
//                         <td>${row.department_line}</td>
//                         <td class="text-end">${row.available}</td>
//                         <td class="text-end">${row.present}</td>
//                         <td class="text-end">${row.absent}</td>
//                         <td class="text-end">${row.absent_pct}%</td>
//                     </tr>
//                 `);
//                 });

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

//     // const loadLateSummary = () => {
//     //         const attendance_date = $date.val() || frappe.datetime.get_today();
//     //         const $tbody = $(wrapper).find('#late-summary-body');
//     //         $tbody.html(`<tr><td colspan="6" style="text-align:center;padding:16px;">Loading…</td></tr>`);

//     //         frappe.call({
//     //             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_late_summary",
//     //             args: { attendance_date },
//     //             callback: function(r) {
//     //                 const data = r.message || [];
//     //                 if (!data.length) {
//     //                     $tbody.html(`<tr><td colspan="6" style="text-align:center;padding:16px;">No data</td></tr>`);
//     //                     return;
//     //                 }

//     //                 // Table rows
//     //                 const rows = data.map(d => `
//     //                     <tr ${d.Description === "Total" ? 'style="font-weight:bold;background:#f9f9f9;"' : ''}>
//     //                         <td style="text-align:center;">${d.Description}</td>
//     //                         <td class="center">${d.STAFF || 0}</td>
//     //                         <td class="center">${d.DIPLOMA || 0}</td>
//     //                         <td class="center">${d.Apprentice || 0}</td>
//     //                         <td class="center">${d.Contract || 0}</td>
//     //                         <td class="center">${d.DRE || 0}</td>
//     //                     </tr>
//     //                 `).join('');
//     //                 $tbody.html(rows);

//     //                 // ✅ Chart (use Total row)
//     //                 const totalRow = data.find(d => d.Description === "Total");
//     //                 if (totalRow) {
//     //                     let categories = [
//     //                         {label: "Staff", count: totalRow.STAFF, color: "#2563eb"},
//     //                         {label: "Diploma", count: totalRow.DIPLOMA, color: "#16a34a"},
//     //                         {label: "Apprentice", count: totalRow.Apprentice, color: "#f59e0b"},
//     //                         {label: "Contract", count: totalRow.Contract, color: "#dc2626"},
//     //                         {label: "DRE", count: totalRow.DRE, color: "#9333ea"},
//     //                     ];

//     //                     let total = categories.reduce((a,b) => a + (b.count||0), 0);
//     //                     let current = 0;
//     //                     let parts = [];

//     //                     categories.forEach(c => {
//     //                         let pct = total ? (c.count/total*100) : 0;
//     //                         parts.push(`${c.color} ${current}% ${current+pct}%`);
//     //                         current += pct;
//     //                     });

//     //                     let circle = document.querySelector(".late-circle");
//     //                     circle.style.background = total > 0 ? 
//     //                         `conic-gradient(${parts.join(",")})` : "#f3f4f6";

//     //                     let labelBox = document.querySelector(".late-label");
//     //                     labelBox.innerHTML = categories.map(c => `
//     //                         <div style="margin:5px;">
//     //                             <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:${c.color};margin-right:6px;"></span>
//     //                             ${c.label}: ${c.count || 0}
//     //                         </div>
//     //                     `).join('');
//     //                 }
//     //             }
//     //         });
//     //     };


//     //     function loadLateSummary() {
//     //         frappe.call({
//     //             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_late_summary",
//     //             callback: function(r) {

//     //                 if (!r.message) return;

//     //                 let data = r.message;

//     //                 let tbody = document.getElementById("late-summary-body");
//     //                 let thead = document.querySelector(".hr-table thead");

//     //                 tbody.innerHTML = "";

//     //                 // get employment types
//     //                 let emp_types = Object.keys(data[0]).filter(
//     //                     key => key !== "Description"
//     //                 );

//     //                 // HEADER BUILD
//     //                 let header_row = `<tr>
//     //                                     <th>Shift/Category</th>`;

//     //                 emp_types.forEach(type => {
//     //                     header_row += `<th>${type}</th>`;
//     //                 });

//     //                 header_row += `</tr>`;

//     //                 thead.innerHTML = header_row;

//     //                 // BODY BUILD
//     //                 data.forEach(row => {

//     //                     let tr = `<tr>`;

//     //                     tr += `<td>${row.Description}</td>`;

//     //                     emp_types.forEach(type => {
//     //                         tr += `<td>${row[type] || 0}</td>`;
//     //                     });

//     //                     tr += `</tr>`;

//     //                     tbody.innerHTML += tr;

//     //                 });

//     //             }
//     //         });
//     // }

// function loadLateSummary() {

//     const attendance_date =
//         document.getElementById("filter-date")?.value ||
//         frappe.datetime.get_today();

//     const tbody = document.getElementById("late-summary-body");

//     tbody.innerHTML = `
//         <tr>
//             <td colspan="6" style="text-align:center;padding:16px;">
//                 Loading...
//             </td>
//         </tr>
//     `;

//     frappe.call({
//         method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_late_summary",
//         args: {
//             attendance_date: attendance_date
//         },
//         callback: function (r) {

//             const data = r.message || [];

//             if (!data.length) {
//                 tbody.innerHTML = `
//                     <tr>
//                         <td colspan="6" style="text-align:center;padding:16px;">
//                             No data
//                         </td>
//                     </tr>
//                 `;
//                 return;
//             }

//             let rows = "";

//             data.forEach(d => {

//                 let style = "";

//                 if (d.Description === "Total") {
//                     style = "font-weight:bold;background:#f3f4f6;";
//                 }

//                 rows += `
//                     <tr style="${style}">
//                         <td>${d.Description || "-"}</td>
//                         <td style="text-align:center">${d.STAFF || 0}</td>
//                         <td style="text-align:center">${d.WORKER || 0}</td>
//                         <td style="text-align:center">${d.NAPS || 0}</td>
//                         <td style="text-align:center">${d.Contract || 0}</td>
//                         <td style="text-align:center">${d.Trainee || 0}</td>
//                     </tr>
//                 `;
//             });

//             tbody.innerHTML = rows;

//         }
//     });

// }

//     // function loadLateSummary() {

//     //     frappe.call({
//     //         method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_late_summary",
//     //         callback: function (r) {

//     //             if (!r.message) return;

//     //             let data = r.message;

//     //             let emp_types = ["STAFF", "WORKER", "NAPS", "Contract", "TRAINEE"];

//     //             let tbody = document.getElementById("late-summary-body");
//     //             let thead = document.querySelector(".hr-table thead");

//     //             tbody.innerHTML = "";

//     //             // TABLE HEADER
//     //             let header = `<tr>
//     //                         <th>Shift/Category</th>`;

//     //             emp_types.forEach(type => {
//     //                 header += `<th>${type}</th>`;
//     //             });

//     //             header += `</tr>`;

//     //             thead.innerHTML = header;

//     //             // TABLE BODY
//     //             data.forEach(row => {

//     //                 let tr = `<tr>`;

//     //                 tr += `<td>${row.Description}</td>`;

//     //                 emp_types.forEach(type => {
//     //                     tr += `<td>${row[type] || 0}</td>`;
//     //                 });

//     //                 tr += `</tr>`;

//     //                 tbody.innerHTML += tr;

//     //             });

//     //         }
//     //     });

//     // }

//     $(wrapper).on('click', '#apply-filter', function () {
//         loadData();
//         loadLeaveSummary();
//         loadHeadCountDetails();
//         loadLateSummary();
//         loadDeptLineSummary();
//     });
//     loadData();
//     loadLateSummary();
//     loadDeptLineSummary();

//     function loadLeaveSummary() {
//         let selected_date = document.getElementById("filter-date").value || frappe.datetime.get_today();

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_leave_summary",
//             args: { attendance_date: selected_date },
//             callback: function (r) {
//                 if (r.message) {
//                     let data = r.message;

//                     let circle = document.querySelector(".leave-circle");
//                     // Update gradient
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


//                 }
//             }
//         });
//     }

//     loadLeaveSummary();
//     loadHeadCountDetails();

//     function loadHeadCountDetails() {
//         let selected_date = document.getElementById("filter-date").value || frappe.datetime.get_today();
//         let selected_shift = document.getElementById("shift").value || "All";

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_headcount_summary",
//             args: { attendance_date: selected_date, shift: selected_shift },
//             // callback: function(r) {
//             //     if (r.message) {
//             //         let data = r.message;

//             //         let circle = document.querySelector(".headcount-circle");
//             //         let gradientParts = [];
//             //         let currentPercent = 0;

//             //         data.categories.forEach((cat, idx) => {
//             //             let nextPercent = currentPercent + cat.percentage;
//             //             let color = cat.color || ["#b131ecff", "#8adf1cff", "#d829acff", "#FF9800"][idx % 4];
//             //             gradientParts.push(`${color} ${currentPercent}% ${nextPercent}%`);
//             //             currentPercent = nextPercent;
//             //         });

//             //         circle.style.background = `conic-gradient(${gradientParts.join(",")})`;

//             //         let labelContainer = document.querySelector(".headcount-label");
//             //         labelContainer.innerHTML = "";
//             //         data.categories.forEach(c => {
//             //             let row = document.createElement("div");
//             //             row.style.display = "flex";
//             //             row.style.alignItems = "center";
//             //             row.style.gap = "10px";
//             //             row.style.marginBottom = "10px";

//             //             let dot = document.createElement("span");
//             //             dot.style.width = "12px";
//             //             dot.style.height = "12px";
//             //             dot.style.borderRadius = "50%";
//             //             dot.style.display = "inline-block";
//             //             dot.style.backgroundColor = c.color;

//             //             let text = document.createElement("span");
//             //             text.innerText = `${c.category}: ${c.count} (${c.percentage.toFixed(1)}%)`;

//             //             row.appendChild(dot);
//             //             row.appendChild(text);
//             //             labelContainer.appendChild(row);
//             //         });
//             //     }
//             // }
//             callback: function (r) {
//                 if (!r.message) return;

//                 let tbody = document.getElementById("dept-summary-body");
//                 tbody.innerHTML = "";

//                 Object.keys(r.message).forEach(dept => {
//                     let d = r.message[dept];

//                     let overall = d.overall || { avail: 0, present: 0, absent: 0 };

//                     let absent_pct = overall.avail
//                         ? ((overall.absent / overall.avail) * 100).toFixed(0)
//                         : 0;

//                     let tr = document.createElement("tr");

//                     tr.innerHTML = `
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

//                     tbody.appendChild(tr);
//                 });
//             }

//         });
//     }

//     function shiftCols(s) {
//         s = s || { plan: 0, present: 0, absent: 0 };

//         return `
//         <td>${s.plan}</td>
//         <td style="color:green">${s.present}</td>
//         <td style="color:red">${s.absent}</td>
//     `;
//     }

//     function loadContractorSummary(date) {
//         let selected_shift = document.getElementById("shift").value || "All";

//         frappe.call({
//             method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_contractor_summary",
//             args: { attendance_date: date, shift: selected_shift },
//             callback: function (r) {
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
//     s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
//     s.onload = function () {

//         let chartInstance;

//         function fetchWeeklyAttendance(from_date, to_date) {
//             frappe.call({
//                 method: "infac.infac.page.hr_dashboard_test.hr_dashboard_test.get_weekly_attendance",
//                 args: { from_date, to_date },
//                 callback: function (r) {
//                     if (!r.message) return;

//                     const data = r.message;
//                     const labels = data.map(d => d.date);
//                     const plan = data.map(d => d.plan);
//                     const actual = data.map(d => d.actual);
//                     const gap = data.map(d => d.gap);
//                     const percent = data.map(d => d.percent);


//                     let rows = "";
//                     data.forEach(d => {
//                         rows += `
//                         <tr>
//                             <td style="text-align:center;background-color:#f5f5f5;">${d.date}</td>
//                             <td style="text-align:center;">${d.plan}</td>
//                             <td style="text-align:center;">${d.actual}</td>
//                             <td style="text-align:center;">${d.gap}</td>
//                             <td style="text-align:center;">${d.percent}%</td>
//                         </tr>`;
//                     });
//                     $('#weekly-attendance-body').html(rows);

//                     const ctx = document.getElementById('weeklyAttendanceChart').getContext('2d');
//                     if (chartInstance) chartInstance.destroy();

//                     chartInstance = new Chart(ctx, {
//                         type: 'line',
//                         data: {
//                             labels: labels,
//                             datasets: [{
//                                 label: '% Attendance',
//                                 data: percent
//                             }]
//                         },
//                         options: {
//                             scales: {
//                                 y: { beginAtZero: true, title: { display: true, text: 'Percentage (%)' } },
//                                 x: { title: { display: true, text: 'Date' } }
//                             }
//                         }
//                     });
//                 }
//             });
//         }

//         const formatDate = d => d.toISOString().split('T')[0];

//         const today = new Date();
//         const next6 = new Date();
//         next6.setDate(today.getDate() + 6);

//         fetchWeeklyAttendance(formatDate(today), formatDate(next6));
//         console.log(formatDate(today))
//         console.log(formatDate(next6))
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
//     document.head.appendChild(s);



// };
frappe.pages['hr-dashboard-test'].on_page_load = function(wrapper) {

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

    function loadHeadCountDetails() {

        const selected_date =
            $(wrapper).find("#filter-date").val() ||
            frappe.datetime.get_today();


        const selected_shift =
            $(wrapper).find("#shift").val() ||
            "All";


        frappe.call({

            method:
                "infac.infac.page.hr_dashboard.hr_dashboard.get_headcount_summary",

            args: {

                attendance_date:
                    selected_date,

                shift:
                    selected_shift

            },

            callback: function(r) {

                if (!r.message) {
                    return;
                }


                const tbody =
                    $(wrapper)
                        .find("#dept-summary-body");


                tbody.empty();


                Object.keys(r.message)
                    .forEach(dept => {

                        const d =
                            r.message[dept];


                        const overall =
                            d.overall || {

                                avail: 0,
                                present: 0,
                                absent: 0

                            };


                        const absent_pct =
                            overall.avail
                                ? (
                                    (
                                        overall.absent /
                                        overall.avail
                                    ) * 100
                                ).toFixed(0)
                                : 0;


                        const tr =
                            document.createElement("tr");


                        tr.innerHTML = `

                            <td>
                                ${frappe.utils.escape_html(
                                    String(dept)
                                )}
                            </td>

                            <td>
                                ${overall.avail}
                            </td>

                            <td style="color:green">
                                ${overall.present}
                            </td>

                            <td style="color:red">
                                ${overall.absent}
                            </td>

                            <td>
                                <b>
                                    ${absent_pct}%
                                </b>
                            </td>

                            ${shiftCols(
                                d["1st Shift"]
                            )}

                            ${shiftCols(
                                d["General"]
                            )}

                            ${shiftCols(
                                d["2nd Shift"]
                            )}

                            ${shiftCols(
                                d["3rd Shift"]
                            )}

                        `;


                        tbody.append(tr);

                    });

            },

            error: function() {

                $(wrapper)
                    .find("#dept-summary-body")
                    .html(`

                        <tr>

                            <td
                                colspan="17"
                                class="text-center text-danger"
                            >
                                Error loading head count
                            </td>

                        </tr>

                    `);

            }

        });

    }


    function shiftCols(s) {

        s =
            s || {

                plan: 0,
                present: 0,
                absent: 0

            };


        return `

            <td>
                ${s.plan}
            </td>

            <td style="color:green">
                ${s.present}
            </td>

            <td style="color:red">
                ${s.absent}
            </td>

        `;

    }


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

    loadDeptLineSummary();

};