// // // // frappe.pages['employee-dashboard'].on_page_load = function(wrapper) {
// // // // 	var page = frappe.ui.make_app_page({
// // // // 		parent: wrapper,
// // // // 		title: 'None',
// // // // 		single_column: true
// // // // 	});
// // // // }

// // // // frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// // // // 	const page = frappe.ui.make_app_page({
// // // // 		parent: wrapper,
// // // // 		title: 'Employee Dashboard',
// // // // 		single_column: true,
// // // // 	});

// // // // 	new EmployeeDashboard(page);
// // // // };

// // // // class EmployeeDashboard {
// // // // 	constructor(page) {
// // // // 		this.page = page;
// // // // 		this.year = new Date().getFullYear();
// // // // 		this.employee = null;

// // // // 		this.inject_styles();
// // // // 		this.setup_toolbar();
// // // // 		this.render_skeleton();
// // // // 		this.set_default_employee();
// // // // 	}

// // // // 	// ---------- Toolbar (employee picker + year picker) ----------
// // // // 	setup_toolbar() {
// // // // 		this.employee_field = this.page.add_field({
// // // // 			label: 'Employee',
// // // // 			fieldname: 'employee',
// // // // 			fieldtype: 'Link',
// // // // 			options: 'Employee',
// // // // 			change: () => {
// // // // 				const val = this.employee_field.get_value();
// // // // 				if (val) {
// // // // 					this.employee = val;
// // // // 					this.load_all();
// // // // 				}
// // // // 			},
// // // // 		});

// // // // 		const year_options = [];
// // // // 		const current_year = new Date().getFullYear();
// // // // 		for (let y = current_year; y >= current_year - 5; y--) year_options.push(String(y));

// // // // 		this.year_field = this.page.add_field({
// // // // 			label: 'Year',
// // // // 			fieldname: 'year',
// // // // 			fieldtype: 'Select',
// // // // 			options: year_options,
// // // // 			default: String(this.year),
// // // // 			change: () => {
// // // // 				this.year = cint(this.year_field.get_value());
// // // // 				this.load_attendance();
// // // // 				this.load_leaves();
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	set_default_employee() {
// // // // 		frappe.db
// // // // 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// // // // 			.then((r) => {
// // // // 				const emp = r && r.message && r.message.name;
// // // // 				if (emp) {
// // // // 					this.employee = emp;
// // // // 					this.employee_field.set_value(emp);
// // // // 				}
// // // // 			});
// // // // 	}

// // // // 	// ---------- Layout ----------
// // // // 	render_skeleton() {
// // // // 		this.$container = $(`
// // // // 			<div class="ed-wrapper">
// // // // 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// // // // 				<div class="ed-card ed-profile-card" style="display:none;"></div>
// // // // 				<div class="ed-card ed-attendance-card" style="display:none;">
// // // // 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// // // // 					<div class="ed-attendance-body"></div>
// // // // 				</div>
// // // // 				<div class="ed-card ed-leave-card" style="display:none;">
// // // // 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// // // // 					<div class="ed-leave-body"></div>
// // // // 				</div>
// // // // 			</div>
// // // // 		`).appendTo(this.page.main);
// // // // 	}

// // // // 	load_all() {
// // // // 		this.$container.find('.ed-empty-state').hide();
// // // // 		this.$container.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card').show();
// // // // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // // // 		this.load_employee();
// // // // 		this.load_attendance();
// // // // 		this.load_leaves();
// // // // 	}

// // // // 	// ---------- Employee profile card ----------
// // // // 	load_employee() {
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// // // // 			args: { employee: this.employee },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_employee_card(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	render_employee_card(e) {
// // // // 		const image = e.image
// // // // 			? `<img src="${e.image}">`
// // // // 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // // // 		const status_color = e.status === 'Active' ? '#2ecc71' : '#95a5a6';

// // // // 		const detail = (label, value) => `
// // // // 			<div class="ed-detail-row">
// // // // 				<div class="ed-detail-label">${label}</div>
// // // // 				<div class="ed-detail-value">${value || '-'}</div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-profile-card').html(`
// // // // 			<div class="ed-profile-header">
// // // // 				<div class="ed-avatar">${image}</div>
// // // // 				<div class="ed-profile-main">
// // // // 					<div class="ed-name-row">
// // // // 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // // // 						<span class="ed-status-pill" style="background:${status_color}22;color:${status_color};">${e.status || ''}</span>
// // // // 					</div>
// // // // 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // // // 					<div class="ed-sub ed-muted">${e.employee}</div>
// // // // 				</div>
// // // // 			</div>
// // // // 			<div class="ed-detail-grid">
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // // // 					${detail('Gender', e.gender)}
// // // // 					${detail('Marital Status', e.marital_status)}
// // // // 					${detail('Blood Group', e.blood_group)}
// // // // 					${detail('Reports To', e.reports_to)}
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // // // 					${detail('Email', e.company_email)}
// // // // 					${detail('Phone', e.cell_number)}
// // // // 					${detail('Address', e.current_address)}
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Aadhaar No.', e.aadhaar_number)}
// // // // 					${detail('PAN No.', e.pan_number)}
// // // // 					${detail('PF No.', e.provident_fund_account)}
// // // // 					${detail('UAN No.', e.uan)}
// // // // 					${detail('ESI No.', e.esic_no)}
// // // // 				</div>
// // // // 			</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Attendance ----------
// // // // 	load_attendance() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_attendance_calendar',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_attendance(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	status_class(status) {
// // // // 		const map = {
// // // // 			Present: 'ed-st-present',
// // // // 			Absent: 'ed-st-absent',
// // // // 			'Half Day': 'ed-st-halfday',
// // // // 			'On Leave': 'ed-st-leave',
// // // // 			'Work From Home': 'ed-st-wfh',
// // // // 			Holiday: 'ed-st-holiday',
// // // // 		};
// // // // 		return map[status] || 'ed-st-other';
// // // // 	}

// // // // 	render_attendance(data) {
// // // // 		// Collect the set of statuses actually seen, to build summary columns dynamically
// // // // 		const status_set = new Set();
// // // // 		data.months.forEach((m) => Object.keys(m.summary).forEach((s) => status_set.add(s)));
// // // // 		const statuses = Array.from(status_set);

// // // // 		// Mini calendars
// // // // 		let calendars = '<div class="ed-calendar-grid">';
// // // // 		data.months.forEach((m) => {
// // // // 			const day_map = {};
// // // // 			m.days.forEach((d) => (day_map[d.day] = d.status));

// // // // 			let cells = '';
// // // // 			for (let d = 1; d <= m.days_in_month; d++) {
// // // // 				const status = day_map[d];
// // // // 				const cls = status ? this.status_class(status) : 'ed-st-none';
// // // // 				cells += `<div class="ed-day-cell ${cls}" title="${status || ''}">${d}</div>`;
// // // // 			}

// // // // 			calendars += `
// // // // 				<div class="ed-mini-month">
// // // // 					<div class="ed-mini-month-title">${m.month_name}</div>
// // // // 					<div class="ed-mini-days">${cells}</div>
// // // // 				</div>`;
// // // // 		});
// // // // 		calendars += '</div>';

// // // // 		// Legend
// // // // 		const legend_items = [
// // // // 			['Present', 'ed-st-present'],
// // // // 			['Absent', 'ed-st-absent'],
// // // // 			['Half Day', 'ed-st-halfday'],
// // // // 			['On Leave', 'ed-st-leave'],
// // // // 			['Work From Home', 'ed-st-wfh'],
// // // // 			['Holiday', 'ed-st-holiday'],
// // // // 		];
// // // // 		const legend = `<div class="ed-legend">${legend_items
// // // // 			.map(([label, cls]) => `<span class="ed-legend-item"><span class="ed-legend-swatch ${cls}"></span>${label}</span>`)
// // // // 			.join('')}</div>`;

// // // // 		// Monthly totals table
// // // // 		let table = `<table class="ed-table"><thead><tr><th>Month</th>${statuses
// // // // 			.map((s) => `<th>${s}</th>`)
// // // // 			.join('')}</tr></thead><tbody>`;
// // // // 		data.months.forEach((m) => {
// // // // 			table += `<tr><td>${m.month_name}</td>${statuses
// // // // 				.map((s) => `<td>${m.summary[s] || '-'}</td>`)
// // // // 				.join('')}</tr>`;
// // // // 		});
// // // // 		// Totals row
// // // // 		const totals = {};
// // // // 		statuses.forEach((s) => (totals[s] = 0));
// // // // 		data.months.forEach((m) => statuses.forEach((s) => (totals[s] += m.summary[s] || 0)));
// // // // 		table += `<tr class="ed-totals-row"><td>Total</td>${statuses
// // // // 			.map((s) => `<td>${totals[s]}</td>`)
// // // // 			.join('')}</tr>`;
// // // // 		table += '</tbody></table>';

// // // // 		this.$container.find('.ed-attendance-body').html(`
// // // // 			${legend}
// // // // 			${calendars}
// // // // 			<div class="ed-table-scroll">${table}</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Leaves ----------
// // // // 	load_leaves() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_leaves(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	render_leaves(data) {
// // // // 		let cards = '';
// // // // 		data.leave_types.forEach((lt) => {
// // // // 			cards += `
// // // // 				<div class="ed-leave-tile">
// // // // 					<div class="ed-leave-tile-title">${lt.leave_type}</div>
// // // // 					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// // // // 					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// // // // 					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// // // // 				</div>`;
// // // // 		});
// // // // 		cards += `
// // // // 			<div class="ed-leave-tile ed-leave-tile-lop">
// // // // 				<div class="ed-leave-tile-title">Loss of Pay</div>
// // // // 				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // // // 	}

// // // // 	// ---------- Styles ----------
// // // // 	// inject_styles() {
// // // // 	// 	if (document.getElementById('ed-styles')) return;
// // // // 	// 	$(`<style id="ed-styles">
// // // // 	// 		.ed-wrapper { max-width: 1180px; margin: 0 auto; padding: 10px 0 40px; }
// // // // 	// 		.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }
// // // // 	// 		.ed-card { background:#fff; border:1px solid #e3e8ee; border-radius:10px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
// // // // 	// 		.ed-profile-card { background: #ead1c9; border-color: #d6e9ff; }
// // // // 	// 		.ed-attendance-card { background: #fef9e7; border-color: #fbeeb8; }
// // // // 	// 		.ed-leave-card { background: #eafaf1; border-color: #c8f0d8; }
// // // // 	// 		.ed-section-title { font-size:15px; font-weight:600; color:#1f2a37; margin-bottom:16px; }

// // // // 	// 		/* profile card */
// // // // 	// 		.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid #eef1f4; margin-bottom:16px; }
// // // // 	// 		.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // // // 	// 		.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#2490ef; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:600; }
// // // // 	// 		.ed-name-row { display:flex; align-items:center; gap:10px; }
// // // // 	// 		.ed-name { font-size:18px; font-weight:700; color:#1f2a37; }
// // // // 	// 		.ed-status-pill { font-size:11px; font-weight:600; padding:2px 10px; border-radius:20px; }
// // // // 	// 		.ed-sub { font-size:13px; color:#5c6b7a; margin-top:2px; }
// // // // 	// 		.ed-muted { color:#a0aab3; }
// // // // 	// 		.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // // // 	// 		.ed-detail-row { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px dashed #eef1f4; font-size:13px; }
// // // // 	// 		.ed-detail-label { color:#8d99a6; }
// // // // 	// 		.ed-detail-value { color:#1f2a37; font-weight:500; text-align:right; max-width:60%; }

// // // // 	// 		/* attendance */
// // // // 	// 		.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:14px; font-size:12px; color:#5c6b7a; }
// // // // 	// 		.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // // 	// 		.ed-legend-swatch { width:12px; height:12px; border-radius:3px; display:inline-block; }
// // // // 	// 		.ed-calendar-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:14px; margin-bottom:22px; }
// // // // 	// 		.ed-mini-month { border:1px solid #eef1f4; border-radius:8px; padding:10px; }
// // // // 	// 		.ed-mini-month-title { font-size:12px; font-weight:600; color:#1f2a37; margin-bottom:8px; text-align:center; }
// // // // 	// 		.ed-mini-days { display:grid; grid-template-columns: repeat(7, 1fr); gap:3px; }
// // // // 	// 		.ed-day-cell { font-size:10px; text-align:center; border-radius:3px; padding:3px 0; color:#4b5563; background:#f4f6f8; }
// // // // 	// 		.ed-st-present { background:#2ecc7133; color:#1e8449; }
// // // // 	// 		.ed-st-absent { background:#e74c3c33; color:#c0392b; }
// // // // 	// 		.ed-st-halfday { background:#f39c1233; color:#af6a08; }
// // // // 	// 		.ed-st-leave { background:#3498db33; color:#1f618d; }
// // // // 	// 		.ed-st-wfh { background:#16a08533; color:#0e6655; }
// // // // 	// 		.ed-st-holiday { background:#8e44ad33; color:#5b2c6f; }
// // // // 	// 		.ed-st-none { background:#f4f6f8; color:#c3cad1; }

// // // // 	// 		.ed-table-scroll { overflow-x:auto; }
// // // // 	// 		.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
// // // // 	// 		.ed-table th, .ed-table td { padding:8px 10px; border-bottom:1px solid #eef1f4; text-align:center; white-space:nowrap; }
// // // // 	// 		.ed-table th { color:#8d99a6; font-weight:600; background:#fafbfc; }
// // // // 	// 		.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
// // // // 	// 		.ed-totals-row td { font-weight:700; color:#1f2a37; background:#fafbfc; }

// // // // 	// 		/* leaves */
// // // // 	// 		.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:14px; }
// // // // 	// 		.ed-leave-tile { border:1px solid #eef1f4; border-radius:8px; padding:14px; background:#fafbfc; }
// // // // 	// 		.ed-leave-tile-lop { background:#fdecea; border-color:#f5c6c1; }
// // // // 	// 		.ed-leave-tile-title { font-size:12.5px; font-weight:600; color:#1f2a37; margin-bottom:8px; }
// // // // 	// 		.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#5c6b7a; padding:2px 0; }
// // // // 	// 		.ed-leave-balance b { color:#2490ef; }
// // // // 	// 	</style>`).appendTo('head');
// // // // 	// }


// // // // 	inject_styles() {
// // // // 		if (document.getElementById('ed-styles')) return;
// // // // 		$(`<style id="ed-styles">
// // // // 			.ed-wrapper { width: 100%; max-width: 1500px; margin: 0 auto; padding: 20px; box-sizing: border-box; background: #f4f6fb; }
// // // // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }
// // // // 			.ed-card { background:#fff; border:1px solid #e3e8ee; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); }

// // // // 			/* card backgrounds — cohesive pastel set */
// // // // 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// // // // 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// // // // 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }

// // // // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; letter-spacing:0.2px; }

// // // // 			/* profile card */
// // // // 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// // // // 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // // // 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:600; box-shadow: 0 4px 10px rgba(99,102,241,0.35); }
// // // // 			.ed-name-row { display:flex; align-items:center; gap:10px; }
// // // // 			.ed-name { font-size:18px; font-weight:700; color:#1e293b; }
// // // // 			.ed-status-pill { font-size:11px; font-weight:600; padding:2px 10px; border-radius:20px; background:#10b98122; color:#059669; }
// // // // 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// // // // 			.ed-muted { color:#94a3b8; }
// // // // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // // // 			.ed-detail-row { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px dashed rgba(99,102,241,0.15); font-size:13px; }
// // // // 			.ed-detail-label { color:#64748b; }
// // // // 			.ed-detail-value { color:#1e293b; font-weight:600; text-align:right; max-width:60%; }

// // // // 			/* attendance */
// // // // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:14px; font-size:12px; color:#78716c; }
// // // // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // // 			.ed-legend-swatch { width:12px; height:12px; border-radius:3px; display:inline-block; }
// // // // 			.ed-calendar-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap:14px; margin-bottom:22px; }
// // // // 			.ed-mini-month { border:1px solid #fed7aa; background:#fff; border-radius:10px; padding:10px; }
// // // // 			.ed-mini-month-title { font-size:12px; font-weight:700; color:#9a3412; margin-bottom:8px; text-align:center; }
// // // // 			.ed-mini-days { display:grid; grid-template-columns: repeat(7, 1fr); gap:3px; }
// // // // 			.ed-day-cell { font-size:10px; text-align:center; border-radius:4px; padding:3px 0; color:#57534e; background:#f5f5f4; }
// // // // 			.ed-st-present { background:#22c55e40; color:#15803d; font-weight:600; }
// // // // 			.ed-st-absent { background:#ef444440; color:#b91c1c; font-weight:600; }
// // // // 			.ed-st-halfday { background:#f59e0b40; color:#b45309; font-weight:600; }
// // // // 			.ed-st-leave { background:#3b82f640; color:#1d4ed8; font-weight:600; }
// // // // 			.ed-st-wfh { background:#14b8a640; color:#0f766e; font-weight:600; }
// // // // 			.ed-st-holiday { background:#a855f740; color:#7e22ce; font-weight:600; }
// // // // 			.ed-st-none { background:#f5f5f4; color:#d6d3d1; }

// // // // 			.ed-table-scroll { overflow-x:auto; }
// // // // 			.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
// // // // 			.ed-table th, .ed-table td { padding:8px 10px; border-bottom:1px solid #fed7aa; text-align:center; white-space:nowrap; }
// // // // 			.ed-table th { color:#9a3412; font-weight:700; background:#fff2e0; }
// // // // 			.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
// // // // 			.ed-totals-row td { font-weight:800; color:#1e293b; background:#fff2e0; }

// // // // 			/* leaves */
// // // // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:14px; }
// // // // 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:14px; background:#fff; }
// // // // 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// // // // 			.ed-leave-tile-title { font-size:12.5px; font-weight:700; color:#065f46; margin-bottom:8px; }
// // // // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:2px 0; }
// // // // 			.ed-leave-balance b { color:#059669; }
// // // // 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

		
// // // // 		</style>`).appendTo('head');
	
// // // // 		}}



// // // frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// // // 	const page = frappe.ui.make_app_page({
// // // 		parent: wrapper,
// // // 		title: 'Employee Dashboard',
// // // 		single_column: true,
// // // 	});

// // // 	new EmployeeDashboard(page);
// // // };

// // // class EmployeeDashboard {
// // // 	constructor(page) {
// // // 		this.page = page;
// // // 		this.year = new Date().getFullYear();
// // // 		this.employee = null;

// // // 		this.inject_styles();
// // // 		this.setup_toolbar();
// // // 		this.render_skeleton();
// // // 		this.set_default_employee();
// // // 	}

// // // 	// ---------- Toolbar (employee picker + year picker) ----------
// // // 	setup_toolbar() {
// // // 		this.employee_field = this.page.add_field({
// // // 			label: 'Employee',
// // // 			fieldname: 'employee',
// // // 			fieldtype: 'Link',
// // // 			options: 'Employee',
// // // 			change: () => {
// // // 				const val = this.employee_field.get_value();
// // // 				if (val) {
// // // 					this.employee = val;
// // // 					this.load_all();
// // // 				}
// // // 			},
// // // 		});

// // // 		const year_options = [];
// // // 		const current_year = new Date().getFullYear();
// // // 		for (let y = current_year; y >= current_year - 5; y--) year_options.push(String(y));

// // // 		this.year_field = this.page.add_field({
// // // 			label: 'Year',
// // // 			fieldname: 'year',
// // // 			fieldtype: 'Select',
// // // 			options: year_options,
// // // 			default: String(this.year),
// // // 			change: () => {
// // // 				this.update_year();
// // // 			},
// // // 		});

// // // 		// fallback: Frappe's df.change callback doesn't always fire reliably
// // // 		// for Select fields, so also bind directly to the native <select>
// // // 		this.year_field.$input.on('change', () => {
// // // 			this.update_year();
// // // 		});
// // // 	}

// // // 	update_year() {
// // //     this.year = cint(this.year_field.get_value());
// // //     this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // //     this.load_attendance();
// // //     this.load_leaves();
// // // }

// // // 	set_default_employee() {
// // // 		frappe.db
// // // 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// // // 			.then((r) => {
// // // 				const emp = r && r.message && r.message.name;
// // // 				if (emp) {
// // // 					this.employee = emp;
// // // 					this.employee_field.set_value(emp);
// // // 				}
// // // 			});
// // // 	}

// // // 	// ---------- Layout ----------
// // // 	render_skeleton() {
// // // 		this.$container = $(`
// // // 			<div class="ed-wrapper">
// // // 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// // // 				<div class="ed-card ed-profile-card" style="display:none;"></div>
// // // 				<div class="ed-card ed-attendance-card" style="display:none;">
// // // 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// // // 					<div class="ed-attendance-body"></div>
// // // 				</div>
// // // 				<div class="ed-card ed-leave-card" style="display:none;">
// // // 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// // // 					<div class="ed-leave-body"></div>
// // // 				</div>
// // // 			</div>
// // // 		`).appendTo(this.page.main);
// // // 	}

// // // 	load_all() {
// // // 		this.$container.find('.ed-empty-state').hide();
// // // 		this.$container.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card').show();
// // // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // // 		this.load_employee();
// // // 		this.load_attendance();
// // // 		this.load_leaves();
// // // 	}

// // // 	// ---------- Employee profile card ----------
// // // 	load_employee() {
// // // 		frappe.call({
// // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// // // 			args: { employee: this.employee },
// // // 			callback: (r) => {
// // // 				if (r.message) this.render_employee_card(r.message);
// // // 			},
// // // 		});
// // // 	}

// // // 	render_employee_card(e) {
// // // 		const image = e.image
// // // 			? `<img src="${e.image}">`
// // // 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // // 		const is_active = e.status === 'Active';

// // // 		const detail = (label, value) => `
// // // 			<div class="ed-detail-row">
// // // 				<div class="ed-detail-label">${label}</div>
// // // 				<div class="ed-detail-value" title="${value || ''}">${value || '-'}</div>
// // // 			</div>`;

// // // 		this.$container.find('.ed-profile-card').html(`
// // // 			<div class="ed-profile-header">
// // // 				<div class="ed-avatar">${image}</div>
// // // 				<div class="ed-profile-main">
// // // 					<div class="ed-name-row">
// // // 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // // 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// // // 					</div>
// // // 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // // 					<div class="ed-sub ed-muted">${e.employee}</div>
// // // 				</div>
// // // 			</div>
// // // 			<div class="ed-detail-grid">
// // // 				<div class="ed-detail-col">
// // // 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // // 					${detail('Gender', e.gender)}
// // // 					${detail('Marital Status', e.marital_status)}
// // // 					${detail('Blood Group', e.blood_group)}
// // // 					${detail('Reports To', e.reports_to)}
// // // 				</div>
// // // 				<div class="ed-detail-col">
// // // 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // // 					${detail('Email', e.company_email)}
// // // 					${detail('Phone', e.cell_number)}
// // // 					<div class="ed-detail-row">
// // // 						<div class="ed-detail-label">Address</div>
// // // 						<div class="ed-detail-value ed-detail-value-wrap" title="${e.current_address || ''}">${e.current_address || '-'}</div>
// // // 					</div>

// // // 				</div>
// // // 				<div class="ed-detail-col">
// // // 					${detail('Aadhaar No.', e.aadhaar_number)}
// // // 					${detail('PAN No.', e.pan_number)}
// // // 					${detail('PF No.', e.provident_fund_account)}
// // // 					${detail('UAN No.', e.uan)}
// // // 					${detail('ESI No.', e.esic_no)}
// // // 				</div>
// // // 			</div>
// // // 		`);
// // // 	}

// // // 	// ---------- Attendance ----------
// // // 	load_attendance() {
// // // 		if (!this.employee) return;
// // // 		frappe.call({
// // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_payroll_attendance',
// // // 			args: { employee: this.employee, year: this.year },
// // // 			callback: (r) => {
// // // 				if (r.message) this.render_attendance(r.message);
// // // 			},
// // // 		});
// // // 	}

// // // 	render_attendance(data) {
// // // 		const legend_items = [
// // // 			['XX', 'Present', 'att-present'],
// // // 			['AA', 'Absent / LOP', 'att-absent'],
// // // 			['0.5..', 'Half Day', 'att-halfday'],
// // // 			['CL/SL/EL', 'On Leave', 'att-leave'],
// // // 			['HH', 'Holiday', 'att-holiday'],
// // // 			['WW', 'Weekly Off', 'att-weeklyoff'],
// // // 		];
// // // 		const legend = `<div class="ed-legend">${legend_items
// // // 			.map(([code, label, cls]) => `<span class="ed-legend-item"><span class="att-cell-mini ${cls}">${code}</span>${label}</span>`)
// // // 			.join('')}</div>`;

// // // 		const totals_cells = (t, is_header) => `
// // // 			<div class="att-total-cell">${is_header ? 'Cal. Days' : t.calendar_days}</div>
// // // 			<div class="att-total-cell">${is_header ? 'Working Days' : t.working_days}</div>
// // // 			<div class="att-total-cell">${is_header ? 'Worked Days' : t.worked_days}</div>
// // // 			<div class="att-total-cell att-col-ee">${is_header ? 'EE' : (t.ee || '-')}</div>
// // // 			<div class="att-total-cell att-col-cc">${is_header ? 'CC' : (t.cc || '-')}</div>
// // // 			<div class="att-total-cell att-col-ss">${is_header ? 'SS' : (t.ss || '-')}</div>
// // // 			<div class="att-total-cell att-col-splml">${is_header ? 'Spl/ML' : (t.spl_ml || '-')}</div>
// // // 			<div class="att-total-cell att-col-wwhh">${is_header ? 'WW/HH' : t.ww_hh}</div>
// // // 			<div class="att-total-cell">${is_header ? 'Paid Days' : t.paid_days}</div>
// // // 			<div class="att-total-cell att-col-aa">${is_header ? 'AA' : (t.aa || '-')}</div>
// // // 		`;

// // // 		const MAX_DAYS = 31;
// // // 		let rows_html = '';
// // // 		data.rows.forEach((row) => {
// // // 			let day_cells = row.days
// // // 				.map(
// // // 					(d) => `
// // // 					<div class="att-day-col">
// // // 						<div class="att-day-num">${d.day}</div>
// // // 						<div class="att-day-code ${d.css}">${d.code || ''}</div>
// // // 					</div>`
// // // 				)
// // // 				.join('');
// // // 			// pad shorter months (28-30 days) so totals columns stay aligned across rows
// // // 			for (let i = row.days.length; i < MAX_DAYS; i++) {
// // // 				day_cells += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// // // 			}

// // // 			rows_html += `
// // // 				<div class="att-row">
// // // 					<div class="att-month-label">${row.month_name}</div>
// // // 					<div class="att-day-strip">${day_cells}</div>
// // // 					<div class="att-totals-cells">${totals_cells(row.totals, false)}</div>
// // // 				</div>`;
// // // 		});

// // // 		// header/grand rows need the SAME day-strip width as data rows (all filler,
// // // 		// all invisible) so the totals columns line up vertically underneath them
// // // 		let filler_strip = '';
// // // 		for (let i = 0; i < MAX_DAYS; i++) {
// // // 			filler_strip += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// // // 		}

// // // 		const header_row = `
// // // 			<div class="att-row att-header-row">
// // // 				<div class="att-month-label"></div>
// // // 				<div class="att-day-strip">${filler_strip}</div>
// // // 				<div class="att-totals-cells att-totals-header">${totals_cells(null, true)}</div>
// // // 			</div>`;

// // // 		const grand_row = `
// // // 			<div class="att-row att-grand-row">
// // // 				<div class="att-month-label">Total</div>
// // // 				<div class="att-day-strip">${filler_strip}</div>
// // // 				<div class="att-totals-cells">${totals_cells(data.grand_totals, false)}</div>
// // // 			</div>`;

// // // 		this.$container.find('.ed-attendance-body').html(`
// // // 			${legend}
// // // 			<div class="att-table-wrap">
// // // 				${header_row}
// // // 				${rows_html}
// // // 				${grand_row}
// // // 			</div>
// // // 		`);
// // // 	}

// // // 	// ---------- Leaves ----------
// // // 	load_leaves() {
// // // 		if (!this.employee) return;
// // // 		frappe.call({
// // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// // // 			args: { employee: this.employee, year: this.year },
// // // 			callback: (r) => {
// // // 				if (r.message) this.render_leaves(r.message);
// // // 			},
// // // 		});
// // // 	}

// // // 	render_leaves(data) {
// // // 		let cards = '';
// // // 		data.leave_types.forEach((lt) => {
// // // 			cards += `
// // // 				<div class="ed-leave-tile">
// // // 					<div class="ed-leave-tile-title">${lt.leave_type}</div>
// // // 					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// // // 					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// // // 					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// // // 				</div>`;
// // // 		});
// // // 		cards += `
// // // 			<div class="ed-leave-tile ed-leave-tile-lop">
// // // 				<div class="ed-leave-tile-title">Loss of Pay</div>
// // // 				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // // 			</div>`;

// // // 		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // // 	}

// // // 	// ---------- Styles ----------
// // // 	inject_styles() {
// // // 		if (document.getElementById('ed-styles')) return;
// // // 		$(`<style id="ed-styles">
// // // 			.page-content .container,
// // // 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// // // 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// // // 			.ed-wrapper {
// // // 				width: 80%;
// // // 				max-width: 1400px;
// // // 				margin: 0 auto;
// // // 				padding: 20px 0 40px;
// // // 				box-sizing: border-box;
// // // 			}
// // // 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// // // 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// // // 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// // // 			@media (max-width: 640px) {
// // // 				.page-form .form-group,
// // // 				.page-form .frappe-control { width: 100% !important; }
// // // 				.page-form { display:flex; flex-direction:column; gap:4px; }
// // // 			}

// // // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

// // // 			/* ---- card base + per-section color ---- */
// // // 			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
// // // 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// // // 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// // // 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
// // // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; }
// // //  			.ed-detail-value-wrap {
// // //  				white-space: normal !important;
// // //  				overflow: visible !important;
// // //  				text-overflow: unset !important;
// // //  				word-break: break-word;
// // //  				line-height: 1.4;
// // // 			}
// // // 			/* ---- profile card ---- */
// // // 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// // // 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // // 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
// // // 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// // // 			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
// // // 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
// // // 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
// // // 			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
// // // 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// // // 			.ed-muted { color:#94a3b8; }
// // // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // // 			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
// // // 			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
// // // 			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

// // // 			/* ---- attendance: payroll-cycle table ---- */
// // // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// // // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // 			.att-cell-mini { display:inline-block; min-width:26px; text-align:center; font-size:9px; font-weight:700; border-radius:4px; padding:2px 3px; }

// // // 			.att-table-wrap { overflow-x:auto; border-radius:10px; border:1px solid #fed7aa; background:#fff; }
// // // 			.att-row { display:flex; align-items:stretch; border-bottom:1px solid #fed7aa; }
// // // 			.att-row:last-child { border-bottom:none; }
// // // 			.att-month-label { flex:0 0 90px; display:flex; align-items:center; padding:6px 10px; font-size:12px; font-weight:700; color:#9a3412; background:#fff2e0; position:sticky; left:0; z-index:2; }
// // // 			.att-day-strip { display:flex; flex:0 0 auto; }
// // // 			.att-day-col { flex:0 0 26px; width:26px; text-align:center; border-right:1px solid #fef3e2; }
// // // 			.att-day-num { font-size:9px; color:#78716c; padding:3px 0 1px; background:#fffaf0; }
// // // 			.att-day-code { font-size:8.5px; font-weight:700; padding:3px 0; min-height:14px; }
// // // 			.att-day-filler .att-day-num, .att-day-filler .att-day-code { background:transparent; }
// // // 			.att-present { background:#f4f6f8; color:#94a3b8; }
// // // 			.att-absent { background:#ef444455; color:#b91c1c; }
// // // 			.att-halfday { background:#f59e0b55; color:#b45309; }
// // // 			.att-leave { background:#3b82f655; color:#1d4ed8; }
// // // 			.att-holiday { background:#a855f755; color:#7e22ce; }
// // // 			.att-weeklyoff { background:#eab30855; color:#92600a; }
// // // 			.att-wfh { background:#14b8a655; color:#0f766e; }
// // // 			.att-other { background:#e2e8f0; color:#475569; }
// // // 			.att-blank { background:#fff; }

// // // 			.att-totals-cells { display:flex; flex:0 0 auto; }
// // // 			.att-total-cell { flex:0 0 68px; width:68px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#1e293b; border-right:1px solid #fef3e2; padding:0 4px; text-align:center; }
// // // 			.att-totals-header .att-total-cell { font-size:10px; color:#fff; background:#f97316; font-weight:700; padding:8px 4px; }
// // // 			.att-col-ee { color:#6366f1; }
// // // 			.att-col-cc { color:#f97316; }
// // // 			.att-col-ss { color:#14b8a6; }
// // // 			.att-col-splml { color:#ec4899; }
// // // 			.att-col-wwhh { color:#92600a; }
// // // 			.att-col-aa { color:#dc2626; }
// // // 			.att-header-row .att-month-label { background:#fff2e0; }
// // // 			.att-grand-row { background:#fff2e0; font-weight:800; }
// // // 			.att-grand-row .att-total-cell { font-weight:800; }

// // // 			/* ---- leaves ---- */
// // // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
// // // 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
// // // 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// // // 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
// // // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
// // // 			.ed-leave-balance b { color:#059669; font-size:14px; }
// // // 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

// // // 			/* ---- mobile ---- */
// // // 			@media (max-width: 640px) {
// // // 				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
// // // 				.ed-name-row { justify-content: center; }
// // // 				.ed-name { font-size: 17px; }
// // // 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// // // 				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
// // // 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// // // 				.ed-card { padding: 16px; }
// // // 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// // // 				.att-day-col { flex-basis: 22px; width: 22px; }
// // // 				.att-total-cell { flex-basis: 56px; width: 56px; font-size: 10px; }
// // // 				.att-month-label { flex-basis: 70px; font-size: 11px; }
// // // 			}
// // // 		</style>`).appendTo('head');
// // // 	}
// // // }

// // //                  // updated- 07/07---------------------------------------------


// // // // frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// // // // 	const page = frappe.ui.make_app_page({
// // // // 		parent: wrapper,
// // // // 		title: 'Employee Dashboard',
// // // // 		single_column: true,
// // // // 	});

// // // // 	new EmployeeDashboard(page);
// // // // };

// // // // class EmployeeDashboard {
// // // // 	constructor(page) {
// // // // 		this.page = page;
// // // // 		this.year = new Date().getFullYear();
// // // // 		this.employee = null;

// // // // 		this.inject_styles();
// // // // 		this.setup_toolbar();
// // // // 		this.render_skeleton();
// // // // 		this.set_default_employee();
// // // // 	}

// // // // 	// ---------- Toolbar (employee picker + year picker) ----------
// // // // 	setup_toolbar() {
// // // // 		this.employee_field = this.page.add_field({
// // // // 			label: 'Employee',
// // // // 			fieldname: 'employee',
// // // // 			fieldtype: 'Link',
// // // // 			options: 'Employee',
// // // // 			change: () => {
// // // // 				const val = this.employee_field.get_value();
// // // // 				if (val) {
// // // // 					this.employee = val;
// // // // 					this.load_all();
// // // // 				}
// // // // 			},
// // // // 		});

// // // // 		const year_options = [];
// // // // 		const current_year = new Date().getFullYear();
// // // // 		for (let y = current_year; y >= current_year - 5; y--) year_options.push(String(y));

// // // // 		this.year_field = this.page.add_field({
// // // // 			label: 'Year',
// // // // 			fieldname: 'year',
// // // // 			fieldtype: 'Select',
// // // // 			options: year_options,
// // // // 			default: String(this.year),
// // // // 			change: () => {
// // // // 				this.year = cint(this.year_field.get_value());
// // // // 				this.load_attendance();
// // // // 				this.load_leaves();
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	set_default_employee() {
// // // // 		frappe.db
// // // // 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// // // // 			.then((r) => {
// // // // 				const emp = r && r.message && r.message.name;
// // // // 				if (emp) {
// // // // 					this.employee = emp;
// // // // 					this.employee_field.set_value(emp);
// // // // 				}
// // // // 			});
// // // // 	}

// // // // 	// ---------- Layout ----------
// // // // 	render_skeleton() {
// // // // 		this.$container = $(`
// // // // 			<div class="ed-wrapper">
// // // // 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// // // // 				<div class="ed-card ed-profile-card" style="display:none;"></div>
// // // // 				<div class="ed-card ed-attendance-card" style="display:none;">
// // // // 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// // // // 					<div class="ed-attendance-body"></div>
// // // // 				</div>
// // // // 				<div class="ed-card ed-leave-card" style="display:none;">
// // // // 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// // // // 					<div class="ed-leave-body"></div>
// // // // 				</div>
// // // // 			</div>
// // // // 		`).appendTo(this.page.main);
// // // // 	}

// // // // 	load_all() {
// // // // 		this.$container.find('.ed-empty-state').hide();
// // // // 		this.$container.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card').show();
// // // // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // // // 		this.load_employee();
// // // // 		this.load_attendance();
// // // // 		this.load_leaves();
// // // // 	}

// // // // 	// ---------- Employee profile card ----------
// // // // 	load_employee() {
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// // // // 			args: { employee: this.employee },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_employee_card(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	render_employee_card(e) {
// // // // 		const image = e.image
// // // // 			? `<img src="${e.image}">`
// // // // 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // // // 		const is_active = e.status === 'Active';

// // // // 		const detail = (label, value) => `
// // // // 			<div class="ed-detail-row">
// // // // 				<div class="ed-detail-label">${label}</div>
// // // // 				<div class="ed-detail-value" title="${value || ''}">${value || '-'}</div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-profile-card').html(`
// // // // 			<div class="ed-profile-header">
// // // // 				<div class="ed-avatar">${image}</div>
// // // // 				<div class="ed-profile-main">
// // // // 					<div class="ed-name-row">
// // // // 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // // // 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// // // // 					</div>
// // // // 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // // // 					<div class="ed-sub ed-muted">${e.employee}</div>
// // // // 				</div>
// // // // 			</div>
// // // // 			<div class="ed-detail-grid">
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // // // 					${detail('Gender', e.gender)}
// // // // 					${detail('Marital Status', e.marital_status)}
// // // // 					${detail('Blood Group', e.blood_group)}
// // // // 					${detail('Reports To', e.reports_to)}
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // // // 					${detail('Email', e.company_email)}
// // // // 					${detail('Phone', e.cell_number)}
// // // // 					${detail('Address', e.current_address)}
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Aadhaar No.', e.aadhaar_number)}
// // // // 					${detail('PAN No.', e.pan_number)}
// // // // 					${detail('PF No.', e.provident_fund_account)}
// // // // 					${detail('UAN No.', e.uan)}
// // // // 					${detail('ESI No.', e.esic_no)}
// // // // 				</div>
// // // // 			</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Attendance ----------
// // // // 	load_attendance() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_payroll_attendance',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_attendance(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	render_attendance(data) {
// // // // 		const legend_items = [
// // // // 			['XX', 'Present', 'att-present'],
// // // // 			['AA', 'Absent / LOP', 'att-absent'],
// // // // 			['0.5..', 'Half Day', 'att-halfday'],
// // // // 			['CL/SL/EL', 'On Leave', 'att-leave'],
// // // // 			['HH', 'Holiday', 'att-holiday'],
// // // // 			['WW', 'Weekly Off', 'att-weeklyoff'],
// // // // 		];
// // // // 		const legend = `<div class="ed-legend">${legend_items
// // // // 			.map(([code, label, cls]) => `<span class="ed-legend-item"><span class="att-cell-mini ${cls}">${code}</span>${label}</span>`)
// // // // 			.join('')}</div>`;

// // // // 		const totals_cells = (t, is_header) => `
// // // // 			<div class="att-total-cell">${is_header ? 'Cal. Days' : t.calendar_days}</div>
// // // // 			<div class="att-total-cell">${is_header ? 'Working Days' : t.working_days}</div>
// // // // 			<div class="att-total-cell">${is_header ? 'Worked Days' : t.worked_days}</div>
// // // // 			<div class="att-total-cell att-col-ee">${is_header ? 'EE' : (t.ee || '-')}</div>
// // // // 			<div class="att-total-cell att-col-cc">${is_header ? 'CC' : (t.cc || '-')}</div>
// // // // 			<div class="att-total-cell att-col-ss">${is_header ? 'SS' : (t.ss || '-')}</div>
// // // // 			<div class="att-total-cell att-col-splml">${is_header ? 'Spl/ML' : (t.spl_ml || '-')}</div>
// // // // 			<div class="att-total-cell att-col-wwhh">${is_header ? 'WW/HH' : t.ww_hh}</div>
// // // // 			<div class="att-total-cell">${is_header ? 'Paid Days' : t.paid_days}</div>
// // // // 			<div class="att-total-cell att-col-aa">${is_header ? 'AA' : (t.aa || '-')}</div>
// // // // 		`;

// // // // 		const MAX_DAYS = 31;
// // // // 		let rows_html = '';
// // // // 		data.rows.forEach((row) => {
// // // // 			let day_cells = row.days
// // // // 				.map(
// // // // 					(d) => `
// // // // 					<div class="att-day-col">
// // // // 						<div class="att-day-num">${d.day}</div>
// // // // 						<div class="att-day-code ${d.css}">${d.code || ''}</div>
// // // // 					</div>`
// // // // 				)
// // // // 				.join('');
// // // // 			// pad shorter months (28-30 days) so totals columns stay aligned across rows
// // // // 			for (let i = row.days.length; i < MAX_DAYS; i++) {
// // // // 				day_cells += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// // // // 			}

// // // // 			rows_html += `
// // // // 				<div class="att-row">
// // // // 					<div class="att-month-label">${row.month_name}</div>
// // // // 					<div class="att-day-strip">${day_cells}</div>
// // // // 					<div class="att-totals-cells">${totals_cells(row.totals, false)}</div>
// // // // 				</div>`;
// // // // 		});

// // // // 		const header_row = `
// // // // 			<div class="att-row att-header-row">
// // // // 				<div class="att-month-label"></div>
// // // // 				<div class="att-day-strip"></div>
// // // // 				<div class="att-totals-cells att-totals-header">${totals_cells(null, true)}</div>
// // // // 			</div>`;

// // // // 		const grand_row = `
// // // // 			<div class="att-row att-grand-row">
// // // // 				<div class="att-month-label">Total</div>
// // // // 				<div class="att-day-strip"></div>
// // // // 				<div class="att-totals-cells">${totals_cells(data.grand_totals, false)}</div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-attendance-body').html(`
// // // // 			${legend}
// // // // 			<div class="att-table-wrap">
// // // // 				${header_row}
// // // // 				${rows_html}
// // // // 				${grand_row}
// // // // 			</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Leaves ----------
// // // // 	load_leaves() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_leaves(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	render_leaves(data) {
// // // // 		let cards = '';
// // // // 		data.leave_types.forEach((lt) => {
// // // // 			cards += `
// // // // 				<div class="ed-leave-tile">
// // // // 					<div class="ed-leave-tile-title">${lt.leave_type}</div>
// // // // 					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// // // // 					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// // // // 					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// // // // 				</div>`;
// // // // 		});
// // // // 		cards += `
// // // // 			<div class="ed-leave-tile ed-leave-tile-lop">
// // // // 				<div class="ed-leave-tile-title">Loss of Pay</div>
// // // // 				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // // // 	}

// // // // 	// ---------- Styles ----------
// // // // 	inject_styles() {
// // // // 		if (document.getElementById('ed-styles')) return;
// // // // 		$(`<style id="ed-styles">
// // // // 			.page-content .container,
// // // // 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// // // // 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// // // // 			.ed-wrapper {
// // // // 				width: 80%;
// // // // 				max-width: 1400px;
// // // // 				margin: 0 auto;
// // // // 				padding: 20px 0 40px;
// // // // 				box-sizing: border-box;
// // // // 			}
// // // // 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// // // // 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// // // // 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// // // // 			@media (max-width: 640px) {
// // // // 				.page-form .form-group,
// // // // 				.page-form .frappe-control { width: 100% !important; }
// // // // 				.page-form { display:flex; flex-direction:column; gap:4px; }
// // // // 			}

// // // // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

// // // // 			/* ---- card base + per-section color ---- */
// // // // 			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
// // // // 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// // // // 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// // // // 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
// // // // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; }

// // // // 			/* ---- profile card ---- */
// // // // 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// // // // 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // // // 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
// // // // 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// // // // 			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
// // // // 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
// // // // 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
// // // // 			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
// // // // 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// // // // 			.ed-muted { color:#94a3b8; }
// // // // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // // // 			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
// // // // 			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
// // // // 			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

// // // // 			/* ---- attendance: payroll-cycle table ---- */
// // // // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// // // // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // // 			.att-cell-mini { display:inline-block; min-width:26px; text-align:center; font-size:9px; font-weight:700; border-radius:4px; padding:2px 3px; }

// // // // 			.att-table-wrap { overflow-x:auto; border-radius:10px; border:1px solid #fed7aa; background:#fff; }
// // // // 			.att-row { display:flex; align-items:stretch; border-bottom:1px solid #fed7aa; }
// // // // 			.att-row:last-child { border-bottom:none; }
// // // // 			.att-month-label { flex:0 0 90px; display:flex; align-items:center; padding:6px 10px; font-size:12px; font-weight:700; color:#9a3412; background:#fff2e0; position:sticky; left:0; z-index:2; }
// // // // 			.att-day-strip { display:flex; flex:0 0 auto; }
// // // // 			.att-day-col { flex:0 0 26px; width:26px; text-align:center; border-right:1px solid #fef3e2; }
// // // // 			.att-day-num { font-size:9px; color:#78716c; padding:3px 0 1px; background:#fffaf0; }
// // // // 			.att-day-code { font-size:8.5px; font-weight:700; padding:3px 0; min-height:14px; }
// // // // 			.att-day-filler .att-day-num, .att-day-filler .att-day-code { background:transparent; }
// // // // 			.att-present { background:#f4f6f8; color:#94a3b8; }
// // // // 			.att-absent { background:#ef444455; color:#b91c1c; }
// // // // 			.att-halfday { background:#f59e0b55; color:#b45309; }
// // // // 			.att-leave { background:#3b82f655; color:#1d4ed8; }
// // // // 			.att-holiday { background:#a855f755; color:#7e22ce; }
// // // // 			.att-weeklyoff { background:#eab30855; color:#92600a; }
// // // // 			.att-wfh { background:#14b8a655; color:#0f766e; }
// // // // 			.att-other { background:#e2e8f0; color:#475569; }
// // // // 			.att-blank { background:#fff; }

// // // // 			.att-totals-cells { display:flex; flex:0 0 auto; }
// // // // 			.att-total-cell { flex:0 0 68px; width:68px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#1e293b; border-right:1px solid #fef3e2; padding:0 4px; text-align:center; }
// // // // 			.att-totals-header .att-total-cell { font-size:10px; color:#fff; background:#f97316; font-weight:700; padding:8px 4px; }
// // // // 			.att-col-ee { color:#6366f1; }
// // // // 			.att-col-cc { color:#f97316; }
// // // // 			.att-col-ss { color:#14b8a6; }
// // // // 			.att-col-splml { color:#ec4899; }
// // // // 			.att-col-wwhh { color:#92600a; }
// // // // 			.att-col-aa { color:#dc2626; }
// // // // 			.att-header-row .att-month-label { background:#fff2e0; }
// // // // 			.att-grand-row { background:#fff2e0; font-weight:800; }
// // // // 			.att-grand-row .att-total-cell { font-weight:800; }

// // // // 			/* ---- leaves ---- */
// // // // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
// // // // 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
// // // // 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// // // // 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
// // // // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
// // // // 			.ed-leave-balance b { color:#059669; font-size:14px; }
// // // // 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

// // // // 			/* ---- mobile ---- */
// // // // 			@media (max-width: 640px) {
// // // // 				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
// // // // 				.ed-name-row { justify-content: center; }
// // // // 				.ed-name { font-size: 17px; }
// // // // 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// // // // 				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
// // // // 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// // // // 				.ed-card { padding: 16px; }
// // // // 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// // // // 				.att-day-col { flex-basis: 22px; width: 22px; }
// // // // 				.att-total-cell { flex-basis: 56px; width: 56px; font-size: 10px; }
// // // // 				.att-month-label { flex-basis: 70px; font-size: 11px; }
// // // // 			}
// // // // 		</style>`).appendTo('head');
// // // // 	}
// // // // }



// // // // frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// // // // 	const page = frappe.ui.make_app_page({
// // // // 		parent: wrapper,
// // // // 		title: 'Employee Dashboard',
// // // // 		single_column: true,
// // // // 	});

// // // // 	new EmployeeDashboard(page);
// // // // };

// // // // class EmployeeDashboard {
// // // // 	constructor(page) {
// // // // 		this.page = page;
// // // // 		this.year = new Date().getFullYear();
// // // // 		this.employee = null;

// // // // 		this.inject_styles();
// // // // 		this.setup_toolbar();
// // // // 		this.render_skeleton();
// // // // 		this.set_default_employee();
// // // // 	}

// // // // 	// ---------- Toolbar (employee picker + year picker) ----------
// // // // 	setup_toolbar() {
// // // // 		this.employee_field = this.page.add_field({
// // // // 			label: 'Employee',
// // // // 			fieldname: 'employee',
// // // // 			fieldtype: 'Link',
// // // // 			options: 'Employee',
// // // // 			change: () => {
// // // // 				const val = this.employee_field.get_value();
// // // // 				if (val) {
// // // // 					this.employee = val;
// // // // 					this.load_all();
// // // // 				}
// // // // 			},
// // // // 		});

		

// // // // 		const year_options = [];
// // // // 		const current_year = new Date().getFullYear();
// // // // 		for (let y = current_year; y >= current_year - 5; y--) year_options.push(String(y));

// // // // 		// this.year_field = this.page.add_field({
// // // // 		// 	label: 'Year',
// // // // 		// 	fieldname: 'year',
// // // // 		// 	fieldtype: 'Select',
// // // // 		// 	options: year_options,
// // // // 		// 	default: String(this.year),
// // // // 		// 	change: () => {
// // // // 		// 		this.year = cint(this.year_field.get_value());
// // // // 		// 		this.load_attendance();
// // // // 		// 		this.load_leaves();
// // // // 		// 	},
// // // // 		// });

// // // // 		this.year_field = this.page.add_field({
// // // // 			label: 'Year',
// // // // 			fieldname: 'year',
// // // // 			fieldtype: 'Select',
// // // // 			options: year_options,
// // // // 			default: String(this.year),
// // // // 			change: () => {
// // // // 				this.update_year();
// // // // 			},
// // // // 		});
// // // // 		this.year_field.$input.on('change', () => {
// // // // 		this.update_year();
// // // // 	});
// // // // 	}

// // // // 	update_year() {
// // // // 		this.year = cint(this.year_field.get_value());
// // // // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // // // 		this.load_attendance();
// // // // 		this.load_leaves();
// // // // 	}

// // // // 	set_default_employee() {
// // // // 		frappe.db
// // // // 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// // // // 			.then((r) => {
// // // // 				const emp = r && r.message && r.message.name;
// // // // 				if (emp) {
// // // // 					this.employee = emp;
// // // // 					this.employee_field.set_value(emp);
// // // // 				}
// // // // 			});
// // // // 	}

// // // // 	// ---------- Layout ----------
// // // // 	render_skeleton() {
// // // // 		this.$container = $(`
// // // // 			<div class="ed-wrapper">
// // // // 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// // // // 				<div class="ed-card ed-profile-card" style="display:none;"></div>
// // // // 				<div class="ed-card ed-attendance-card" style="display:none;">
// // // // 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// // // // 					<div class="ed-attendance-body"></div>
// // // // 				</div>
// // // // 				<div class="ed-card ed-leave-card" style="display:none;">
// // // // 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// // // // 					<div class="ed-leave-body"></div>
// // // // 				</div>
// // // // 			</div>
// // // // 		`).appendTo(this.page.main);
// // // // 	}

// // // // 	load_all() {
// // // // 		this.$container.find('.ed-empty-state').hide();
// // // // 		this.$container.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card').show();
// // // // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // // // 		this.load_employee();
// // // // 		this.load_attendance();
// // // // 		this.load_leaves();
// // // // 	}

// // // // 	// ---------- Employee profile card ----------
// // // // 	load_employee() {
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// // // // 			args: { employee: this.employee },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_employee_card(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	// render_employee_card(e) {
// // // // 	// 	const image = e.image
// // // // 	// 		? `<img src="${e.image}">`
// // // // 	// 		: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // // // 	// 	const is_active = e.status === 'Active';

// // // // 	// 	const detail = (label, value) => `
// // // // 	// 		<div class="ed-detail-row">
// // // // 	// 			<div class="ed-detail-label">${label}</div>
// // // // 	// 			<div class="ed-detail-value">${value || '-'}</div>
// // // // 	// 		</div>`;

// // // // 	// 	this.$container.find('.ed-profile-card').html(`
// // // // 	// 		<div class="ed-hero">
// // // // 	// 			<div class="ed-hero-blob"></div>
// // // // 	// 			<div class="ed-hero-content">
// // // // 	// 				<div class="ed-avatar">${image}</div>
// // // // 	// 				<div class="ed-hero-main">
// // // // 	// 					<div class="ed-name-row">
// // // // 	// 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // // // 	// 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// // // // 	// 					</div>
// // // // 	// 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // // // 	// 					<div class="ed-sub ed-muted">ID: ${e.employee}</div>
// // // // 	// 				</div>
// // // // 	// 			</div>
// // // // 	// 		</div>
// // // // 	// 		<div class="ed-detail-grid">
// // // // 	// 			<div class="ed-detail-col">
// // // // 	// 				${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // // // 	// 				${detail('Gender', e.gender)}
// // // // 	// 				${detail('Marital Status', e.marital_status)}
// // // // 	// 				${detail('Blood Group', e.blood_group)}
// // // // 	// 				${detail('Reports To', e.reports_to)}
// // // // 	// 			</div>
// // // // 	// 			<div class="ed-detail-col">
// // // // 	// 				${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // // // 	// 				${detail('Email', e.company_email)}
// // // // 	// 				${detail('Phone', e.cell_number)}
// // // // 	// 				${detail('Address', e.current_address)}
// // // // 	// 			</div>
// // // // 	// 			<div class="ed-detail-col">
// // // // 	// 				${detail('Aadhaar No.', e.aadhaar_number)}
// // // // 	// 				${detail('PAN No.', e.pan_number)}
// // // // 	// 				${detail('PF No.', e.provident_fund_account)}
// // // // 	// 				${detail('UAN No.', e.uan)}
// // // // 	// 				${detail('ESI No.', e.esic_no)}
// // // // 	// 			</div>
// // // // 	// 		</div>
// // // // 	// 	`);
// // // // 	// }


	
// // // // 	render_employee_card(e) {
// // // // 		const image = e.image
// // // // 			? `<img src="${e.image}">`
// // // // 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // // // 		const is_active = e.status === 'Active';

// // // // 		const detail = (label, value) => `
// // // // 			<div class="ed-detail-row">
// // // // 				<div class="ed-detail-label">${label}</div>
// // // // 				<div class="ed-detail-value">${value || '-'}</div>
// // // // 			</div>`;

// // // // 		this.$container.find('.ed-profile-card').html(`
// // // // 			<div class="ed-profile-header">
// // // // 				<div class="ed-avatar">${image}</div>
// // // // 				<div class="ed-profile-main">
// // // // 					<div class="ed-name-row">
// // // // 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // // // 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// // // // 					</div>
// // // // 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // // // 					<div class="ed-sub ed-muted">${e.employee}</div>
// // // // 				</div>
// // // // 			</div>
// // // // 			<div class="ed-detail-grid">
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // // // 					${detail('Gender', e.gender)}
// // // // 					${detail('Marital Status', e.marital_status)}
// // // // 					${detail('Blood Group', e.blood_group)}
// // // // 					${detail('Reports To', e.reports_to)}
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // // // 					${detail('Email', e.company_email)}
// // // // 					${detail('Phone', e.cell_number)}
// // // // 					<div class="ed-detail-row">
// // // // 						<div class="ed-detail-label">Address</div>
// // // // 						<div class="ed-detail-value ed-detail-value-wrap" title="${e.current_address || ''}">${e.current_address || '-'}</div>
// // // // 					</div>
// // // // 				</div>
// // // // 				<div class="ed-detail-col">
// // // // 					${detail('Aadhaar No.', e.aadhaar_number)}
// // // // 					${detail('PAN No.', e.pan_number)}
// // // // 					${detail('PF No.', e.provident_fund_account)}
// // // // 					${detail('UAN No.', e.uan)}
// // // // 					${detail('ESI No.', e.esic_no)}
// // // // 				</div>
// // // // 			</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Attendance ----------
// // // // 	load_attendance() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_attendance_calendar',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_attendance(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	status_class(status) {
// // // // 		const map = {
// // // // 			Present: 'ed-st-present',
// // // // 			Absent: 'ed-st-absent',
// // // // 			'Half Day': 'ed-st-halfday',
// // // // 			'On Leave': 'ed-st-leave',
// // // // 			'Work From Home': 'ed-st-wfh',
// // // // 			Holiday: 'ed-st-holiday',
// // // // 		};
// // // // 		return map[status] || 'ed-st-other';
// // // // 	}

// // // // 	render_attendance(data) {
// // // // 		// Collect the set of statuses actually seen, to build summary columns dynamically
// // // // 		const status_set = new Set();
// // // // 		data.months.forEach((m) => Object.keys(m.summary).forEach((s) => status_set.add(s)));
// // // // 		const statuses = Array.from(status_set);

// // // // 		// Mini calendars
// // // // 		let calendars = '<div class="ed-calendar-grid">';
// // // // 		data.months.forEach((m) => {
// // // // 			const day_map = {};
// // // // 			m.days.forEach((d) => (day_map[d.day] = d.status));

// // // // 			let cells = '';
// // // // 			for (let d = 1; d <= m.days_in_month; d++) {
// // // // 				const status = day_map[d];
// // // // 				const cls = status ? this.status_class(status) : 'ed-st-none';
// // // // 				cells += `<div class="ed-day-cell ${cls}" title="${status || ''}">${d}</div>`;
// // // // 			}

// // // // 			calendars += `
// // // // 				<div class="ed-mini-month">
// // // // 					<div class="ed-mini-month-title">${m.month_name}</div>
// // // // 					<div class="ed-mini-days">${cells}</div>
// // // // 				</div>`;
// // // // 		});
// // // // 		calendars += '</div>';

// // // // 		// Legend
// // // // 		const legend_items = [
// // // // 			['Present', 'ed-st-present'],
// // // // 			['Absent', 'ed-st-absent'],
// // // // 			['Half Day', 'ed-st-halfday'],
// // // // 			['On Leave', 'ed-st-leave'],
// // // // 			['Work From Home', 'ed-st-wfh'],
// // // // 			['Holiday', 'ed-st-holiday'],
// // // // 		];
// // // // 		const legend = `<div class="ed-legend">${legend_items
// // // // 			.map(([label, cls]) => `<span class="ed-legend-item"><span class="ed-legend-swatch ${cls}"></span>${label}</span>`)
// // // // 			.join('')}</div>`;

// // // // 		// Monthly totals table
// // // // 		// let table = `<table class="ed-table"><thead><tr><th>Month</th>${statuses
// // // // 		// 	.map((s) => `<th>${s}</th>`)
// // // // 		// 	.join('')}</tr></thead><tbody>`;
// // // // 		// data.months.forEach((m) => {
// // // // 		// 	table += `<tr><td>${m.month_name}</td>${statuses
// // // // 		// 		.map((s) => `<td>${m.summary[s] || '-'}</td>`)
// // // // 		// 		.join('')}</tr>`;
// // // // 		// });
// // // // 		// // Totals row
// // // // 		// const totals = {};
// // // // 		// statuses.forEach((s) => (totals[s] = 0));
// // // // 		// data.months.forEach((m) => statuses.forEach((s) => (totals[s] += m.summary[s] || 0)));
// // // // 		// table += `<tr class="ed-totals-row"><td>Total</td>${statuses
// // // // 		// 	.map((s) => `<td>${totals[s]}</td>`)
// // // // 		// 	.join('')}</tr>`;
// // // // 		// table += '</tbody></table>';

// // // // 		// Monthly totals table
// // // // let table = `<table class="ed-table"><thead><tr><th>Month</th><th>Calendar Days</th>${statuses
// // // //     .map((s) => `<th>${s}</th>`)
// // // //     .join('')}</tr></thead><tbody>`;
// // // // data.months.forEach((m) => {
// // // //     table += `<tr><td>${m.month_name}</td><td>${m.days_in_month}</td>${statuses
// // // //         .map((s) => `<td>${m.summary[s] || '-'}</td>`)
// // // //         .join('')}</tr>`;
// // // // });
// // // // // Totals row
// // // // const totals = {};
// // // // statuses.forEach((s) => (totals[s] = 0));
// // // // let total_calendar_days = 0;
// // // // data.months.forEach((m) => {
// // // //     total_calendar_days += m.days_in_month;
// // // //     statuses.forEach((s) => (totals[s] += m.summary[s] || 0));
// // // // });
// // // // table += `<tr class="ed-totals-row"><td>Total</td><td>${total_calendar_days}</td>${statuses
// // // //     .map((s) => `<td>${totals[s]}</td>`)
// // // //     .join('')}</tr>`;
// // // // table += '</tbody></table>';

// // // // 		this.$container.find('.ed-attendance-body').html(`
// // // // 			${legend}
// // // // 			${calendars}
// // // // 			<div class="ed-table-scroll">${table}</div>
// // // // 		`);
// // // // 	}

// // // // 	// ---------- Leaves ----------
// // // // 	load_leaves() {
// // // // 		if (!this.employee) return;
// // // // 		frappe.call({
// // // // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// // // // 			args: { employee: this.employee, year: this.year },
// // // // 			callback: (r) => {
// // // // 				if (r.message) this.render_leaves(r.message);
// // // // 			},
// // // // 		});
// // // // 	}

// // // // 	// render_leaves(data) {
// // // // 	// 	const palette = ['#6366f1', '#f97316', '#14b8a6', '#ec4899', '#eab308', '#3b82f6'];
// // // // 	// 	let cards = '';
// // // // 	// 	data.leave_types.forEach((lt, idx) => {
// // // // 	// 		const color = palette[idx % palette.length];
// // // // 	// 		const total = (lt.allocated || 0) > 0 ? lt.allocated : (lt.taken || 0) || 1;
// // // // 	// 		const pct = Math.min(100, Math.round(((lt.taken || 0) / total) * 100));
// // // // 	// 		cards += `
// // // // 	// 			<div class="ed-leave-tile" style="--ed-accent:${color};">
// // // // 	// 				<div class="ed-leave-tile-title">${lt.leave_type}</div>
// // // // 	// 				<div class="ed-leave-bar-track">
// // // // 	// 					<div class="ed-leave-bar-fill" style="width:${pct}%;background:${color};"></div>
// // // // 	// 				</div>
// // // // 	// 				<div class="ed-leave-tile-row"><span>Taken ${lt.taken} / ${lt.allocated}</span><b style="color:${color};">${lt.balance} left</b></div>
// // // // 	// 			</div>`;
// // // // 	// 	});
// // // // 	// 	cards += `
// // // // 	// 		<div class="ed-leave-tile ed-leave-tile-lop" style="--ed-accent:#ef4444;">
// // // // 	// 			<div class="ed-leave-tile-title">Loss of Pay</div>
// // // // 	// 			<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // // // 	// 		</div>`;

// // // // 	// 	this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // // // 	// }


// // // // 	render_leaves(data) {
// // // //     let cards = '';
// // // //     data.leave_types.forEach((lt) => {
// // // //         cards += `
// // // //             <div class="ed-leave-tile">
// // // //                 <div class="ed-leave-tile-title">${lt.leave_type}</div>
// // // //                 <div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// // // //                 <div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// // // //                 <div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// // // //             </div>`;
// // // //     });
// // // //     cards += `
// // // //         <div class="ed-leave-tile ed-leave-tile-lop">
// // // //             <div class="ed-leave-tile-title">Loss of Pay</div>
// // // //             <div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // // //         </div>`;

// // // //     this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // // // }
// // // // 	// ---------- Styles ----------
	
	
// // // // // 	inject_styles() {
// // // // // 		if (document.getElementById('ed-styles')) return;
// // // // // 		$(`<style id="ed-styles">
// // // // // 			.page-content .container,
// // // // // 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// // // // // 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// // // // // 			.ed-wrapper {
// // // // // 				width: 80%;
// // // // // 				max-width: 1400px;
// // // // // 				margin: 0 auto;
// // // // // 				padding: 20px 0 40px;
// // // // // 				box-sizing: border-box;
// // // // // 			}
// // // // // 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// // // // // 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// // // // // 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// // // // // 			@media (max-width: 640px) {
// // // // // 				.page-form .form-group,
// // // // // 				.page-form .frappe-control { width: 100% !important; }
// // // // // 				.page-form { display:flex; flex-direction:column; gap:4px; }
// // // // // 			}
// // // // // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }
// // // // // 			.ed-card { background:#fff; border-radius:16px; padding:0; margin-bottom:22px; box-shadow: 0 4px 18px rgba(30,41,59,0.06); overflow:hidden; }
// // // // // 			.ed-attendance-card, .ed-leave-card { padding:22px 26px; }
// // // // // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
// // // // // 			.ed-section-title::before { content:''; width:5px; height:16px; border-radius:3px; background:#6366f1; display:inline-block; }
// // // // // 			.ed-attendance-card .ed-section-title::before { background:#f97316; }
// // // // // 			.ed-leave-card .ed-section-title::before { background:#10b981; }

// // // // // 			/* ---- profile hero ---- */
// // // // // 			.ed-hero {
// // // // // 				position:relative;
// // // // // 				padding: 28px 28px 22px;
// // // // // 				background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #c026d3 100%);
// // // // // 				color:#fff;
// // // // // 				overflow:hidden;
// // // // // 			}
// // // // // 			.ed-hero-blob {
// // // // // 				position:absolute; top:-60px; right:-60px; width:220px; height:220px; border-radius:50%;
// // // // // 				background: rgba(255,255,255,0.08);
// // // // // 			}
// // // // // 			.ed-hero-content { display:flex; align-items:center; gap:18px; position:relative; z-index:1; }
// // // // // 			.ed-avatar img { width:72px; height:72px; border-radius:50%; object-fit:cover; border:3px solid rgba(255,255,255,0.8); }
// // // // // 			.ed-avatar-fallback { width:72px; height:72px; border-radius:50%; background:rgba(255,255,255,0.18); border:3px solid rgba(255,255,255,0.7); color:#fff; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:700; backdrop-filter: blur(4px); }
// // // // // 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// // // // // 			.ed-name { font-size:20px; font-weight:800; color:#fff; }
// // // // // 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; text-transform:uppercase; letter-spacing:0.4px; }
// // // // // 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.5); }
// // // // // .ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.5); }
// // // // // 			.ed-hero .ed-sub { font-size:13px; color:rgba(255,255,255,0.85); margin-top:3px; }
// // // // // 			.ed-hero .ed-muted { color:rgba(255,255,255,0.6); }

// // // // // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; padding: 22px 28px 26px; }
// // // // // 			.ed-detail-row { display:flex; align-items:baseline; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:10px; }
// // // // // 			.ed-detail-label { color:#8d99a6; flex: 0 0 auto; white-space: nowrap; }
// // // // // 			.ed-detail-value {
// // // // // 				color:#1e293b;
// // // // // 				font-weight:600;
// // // // // 				text-align:right;
// // // // // 				flex: 1 1 auto;
// // // // // 				min-width: 0;
// // // // // 				white-space: nowrap;
// // // // // 				overflow: hidden;
// // // // // 				text-overflow: ellipsis;
// // // // // 			}
// // // // // 			/* ---- attendance ---- */
// // // // // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// // // // // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // // // 			.ed-legend-swatch { width:12px; height:12px; border-radius:4px; display:inline-block; }
// // // // // 			.ed-calendar-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap:16px; margin-bottom:24px; }
// // // // // 			.ed-mini-month { border-radius:12px; padding:0; background:#fff; box-shadow: 0 2px 10px rgba(30,41,59,0.06); overflow:hidden; }
// // // // // 			.ed-mini-month-title { font-size:12px; font-weight:700; color:#fff; padding:8px 0; text-align:center; background: linear-gradient(120deg,#f97316,#fb923c); }
// // // // // 			.ed-mini-days { display:grid; grid-template-columns: repeat(7, 1fr); gap:4px; padding:10px; }
// // // // // 			.ed-day-cell { font-size:10px; text-align:center; border-radius:6px; padding:4px 0; color:#4b5563; background:#f4f6f8; font-weight:600; }
// // // // // 			.ed-st-present { background:#22c55e40; color:#15803d; }
// // // // // 			.ed-st-absent { background:#ef444440; color:#b91c1c; }
// // // // // 			.ed-st-halfday { background:#f59e0b40; color:#b45309; }
// // // // // 			.ed-st-leave { background:#3b82f640; color:#1d4ed8; }
// // // // // 			.ed-st-wfh { background:#14b8a640; color:#0f766e; }
// // // // // 			.ed-st-holiday { background:#a855f740; color:#7e22ce; }
// // // // // 			.ed-st-none { background:#f4f6f8; color:#c3cad1; }

// // // // // 			.ed-table-scroll { overflow-x:auto; border-radius:10px; }
// // // // // 			.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
// // // // // 			.ed-table th, .ed-table td { padding:9px 10px; border-bottom:1px solid #eef1f4; text-align:center; white-space:nowrap; }
// // // // // 			.ed-table th { color:#fff; font-weight:700; background:#f97316; }
// // // // // 			.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
// // // // // 			.ed-totals-row td { font-weight:800; color:#1e293b; background:#fff7ed; }

// // // // // 			/* ---- leaves ---- */
// // // // // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:16px; }
// // // // // 			.ed-leave-tile { border-radius:12px; padding:16px; background:#fff; box-shadow: 0 2px 10px rgba(30,41,59,0.06); border-top:4px solid var(--ed-accent, #6366f1); }
// // // // // 			.ed-leave-tile-lop { background:#fff5f5; }
// // // // // 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#1e293b; margin-bottom:10px; }
// // // // // 			.ed-leave-bar-track { height:8px; border-radius:6px; background:#f1f5f9; overflow:hidden; margin-bottom:10px; }
// // // // // 			.ed-leave-bar-fill { height:100%; border-radius:6px; transition: width 0.4s ease; }
// // // // // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#64748b; padding:2px 0; }
// // // // // 			.ed-leave-balance b { color:#dc2626; font-size:14px; }

// // // // // 			/* ---- mobile ---- */
// // // // // 			@media (max-width: 640px) {
// // // // // 				.ed-hero { padding: 22px 18px 18px; }
// // // // // 				.ed-hero-content { flex-direction: column; text-align: center; gap: 12px; }
// // // // // 				.ed-name-row { justify-content: center; }
// // // // // 				.ed-name { font-size: 17px; }
// // // // // 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// // // // // 				.ed-detail-grid { grid-template-columns: 1fr; padding: 18px 18px 20px; gap: 0; }
// // // // // 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// // // // // 				.ed-attendance-card, .ed-leave-card { padding: 18px 16px; }
// // // // // 				.ed-calendar-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
// // // // // 				.ed-mini-days { padding: 8px; gap: 3px; }
// // // // // 				.ed-day-cell { font-size: 9px; padding: 3px 0; }
// // // // // 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// // // // // 				.ed-leave-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
// // // // // 				.ed-table { font-size: 11px; }
// // // // // 				.ed-table th, .ed-table td { padding: 6px 6px; }
// // // // // 			}
// // // // // 			@media (max-width: 420px) {
// // // // // 				.ed-calendar-grid { grid-template-columns: 1fr; }
// // // // // 				.ed-leave-grid { grid-template-columns: 1fr; }
// // // // // 			}
// // // // // 		</style>`).appendTo('head');
// // // // // 	}


// // // // 	inject_styles() {
// // // // 		if (document.getElementById('ed-styles')) return;
// // // // 		$(`<style id="ed-styles">
// // // // 			.page-content .container,
// // // // 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// // // // 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// // // // 			.ed-wrapper {
// // // // 				width: 80%;
// // // // 				max-width: 1400px;
// // // // 				margin: 0 auto;
// // // // 				padding: 20px 0 40px;
// // // // 				box-sizing: border-box;
// // // // 			}
// // // // 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// // // // 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// // // // 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// // // // 			@media (max-width: 640px) {
// // // //     .ed-detail-row {
// // // //         flex-direction: column;
// // // //         align-items: flex-start;
// // // //         gap: 2px;
// // // //     }
// // // //     .ed-detail-label {
// // // //         font-size: 11px;
// // // //         text-transform: uppercase;
// // // //         letter-spacing: 0.3px;
// // // //         color: #94a3b8;
// // // //     }
// // // //     .ed-detail-value {
// // // //         text-align: left;
// // // //         white-space: normal;
// // // //         overflow: visible;
// // // //         text-overflow: unset;
// // // //         width: 100%;
// // // //         font-weight: 500;
// // // //     }
// // // // }

// // // // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

// // // // 			/* ---- card base + per-section color ---- */
// // // // 			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
// // // // 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// // // // 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// // // // 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
// // // // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; }
// // // // 			.ed-detail-value-wrap {
// // // // 				white-space: normal !important;
// // // // 				overflow: visible !important;
// // // // 				text-overflow: unset !important;
// // // // 				word-break: break-word;
// // // // 				line-height: 1.4;
// // // // 			}
// // // // 			/* ---- profile card ---- */
// // // // 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// // // // 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // // // 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
// // // // 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// // // // 			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
// // // // 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
// // // // 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
// // // // 			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
// // // // 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// // // // 			.ed-muted { color:#94a3b8; }
// // // // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // // // 			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
// // // // 			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
// // // // 			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

// // // // 			/* ---- attendance ---- */
// // // // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// // // // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // // // 			.ed-legend-swatch { width:12px; height:12px; border-radius:4px; display:inline-block; }
// // // // 			.ed-calendar-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap:16px; margin-bottom:24px; }
// // // // 			.ed-mini-month { border-radius:12px; padding:0; background:#fff; box-shadow: 0 2px 10px rgba(30,41,59,0.06); overflow:hidden; }
// // // // 			.ed-mini-month-title { font-size:12px; font-weight:700; color:#fff; padding:8px 0; text-align:center; background: linear-gradient(120deg,#f97316,#fb923c); }
// // // // 			.ed-mini-days { display:grid; grid-template-columns: repeat(7, 1fr); gap:4px; padding:10px; }
// // // // 			.ed-day-cell { font-size:10px; text-align:center; border-radius:6px; padding:4px 0; color:#4b5563; background:#f4f6f8; font-weight:600; }
// // // // 			.ed-st-present { background:#22c55e40; color:#15803d; }
// // // // 			.ed-st-absent { background:#ef444440; color:#b91c1c; }
// // // // 			.ed-st-halfday { background:#f59e0b40; color:#b45309; }
// // // // 			.ed-st-leave { background:#3b82f640; color:#1d4ed8; }
// // // // 			.ed-st-wfh { background:#14b8a640; color:#0f766e; }
// // // // 			.ed-st-holiday { background:#a855f740; color:#7e22ce; }
// // // // 			.ed-st-none { background:#f4f6f8; color:#c3cad1; }

// // // // 			.ed-table-scroll { overflow-x:auto; border-radius:10px; }
// // // // 			.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
// // // // 			.ed-table th, .ed-table td { padding:9px 10px; border-bottom:1px solid #eef1f4; text-align:center; white-space:nowrap; }
// // // // 			.ed-table th { color:#fff; font-weight:700; background:#f97316; }
// // // // 			.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
// // // // 			.ed-totals-row td { font-weight:800; color:#1e293b; background:#fff7ed; }

// // // // 			/* ---- leaves ---- */
// // // // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
// // // // 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
// // // // 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// // // // 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
// // // // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
// // // // 			.ed-leave-balance b { color:#059669; font-size:14px; }
// // // // 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

// // // // 			/* ---- mobile ---- */
// // // // 			@media (max-width: 640px) {
// // // // 				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
// // // // 				.ed-name-row { justify-content: center; }
// // // // 				.ed-name { font-size: 17px; }
// // // // 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// // // // 				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
// // // // 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// // // // 				.ed-card { padding: 16px; }
// // // // 				.ed-calendar-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
// // // // 				.ed-mini-days { padding: 8px; gap: 3px; }
// // // // 				.ed-day-cell { font-size: 9px; padding: 3px 0; }
// // // // 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// // // // 				.ed-leave-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
// // // // 				.ed-table { font-size: 11px; }
// // // // 				.ed-table th, .ed-table td { padding: 6px 6px; }
// // // // 			}
// // // // 			@media (max-width: 420px) {
// // // // 				.ed-calendar-grid { grid-template-columns: 1fr; }
// // // // 				.ed-leave-grid { grid-template-columns: 1fr; }
// // // // 			}
// // // // 		</style>`).appendTo('head');
// // // // 	}
// // // // }



// // frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// // 	const page = frappe.ui.make_app_page({
// // 		parent: wrapper,
// // 		title: 'Employee Dashboard',
// // 		single_column: true,
// // 	});

// // 	new EmployeeDashboard(page);
// // };

// // class EmployeeDashboard {
// // 	constructor(page) {
// // 		this.page = page;
// // 		this.year = new Date().getFullYear();
// // 		this.employee = null;

// // 		this.inject_styles();
// // 		this.setup_toolbar();
// // 		this.render_skeleton();
// // 		this.set_default_employee();
// // 	}

// // 	// ---------- Toolbar (employee picker + year picker) ----------
// // 	setup_toolbar() {
// // 		this.employee_field = this.page.add_field({
// // 			label: 'Employee',
// // 			fieldname: 'employee',
// // 			fieldtype: 'Link',
// // 			options: 'Employee',
// // 			change: () => {
// // 				const val = this.employee_field.get_value();
// // 				if (val) {
// // 					this.employee = val;
// // 					this.load_all();
// // 				}
// // 			},
// // 		});

// // 		const year_options = [];
// // 		const current_year = new Date().getFullYear();
// // 		for (let y = current_year; y >= current_year - 5; y--) year_options.push(String(y));

// // 		this.year_field = this.page.add_field({
// // 			label: 'Year',
// // 			fieldname: 'year',
// // 			fieldtype: 'Select',
// // 			options: year_options,
// // 			default: String(this.year),
// // 			change: () => {
// // 				this.update_year();
// // 			},
// // 		});

// // 		// fallback: Frappe's df.change callback doesn't always fire reliably
// // 		// for Select fields, so also bind directly to the native <select>
// // 		this.year_field.$input.on('change', () => {
// // 			this.update_year();
// // 		});
// // 	}

// // 	update_year() {
// //     this.year = cint(this.year_field.get_value());
// //     this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// //     this.load_attendance();
// //     this.load_leaves();
// // }

// // 	set_default_employee() {
// // 		frappe.db
// // 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// // 			.then((r) => {
// // 				const emp = r && r.message && r.message.name;
// // 				if (emp) {
// // 					this.employee = emp;
// // 					this.employee_field.set_value(emp);
// // 				}
// // 			});
// // 	}

// // 	// ---------- Layout ----------
// // 	render_skeleton() {
// // 		this.$container = $(`
// // 			<div class="ed-wrapper">
// // 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// // 				<div class="ed-card ed-profile-card" style="display:none;"></div>
// // 				<div class="ed-card ed-attendance-card" style="display:none;">
// // 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// // 					<div class="ed-attendance-body"></div>
// // 				</div>
// // 				<div class="ed-card ed-leave-card" style="display:none;">
// // 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// // 					<div class="ed-leave-body"></div>
// // 				</div>
// // 			</div>
// // 		`).appendTo(this.page.main);
// // 	}

// // 	load_all() {
// // 		this.$container.find('.ed-empty-state').hide();
// // 		this.$container.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card').show();
// // 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// // 		this.load_employee();
// // 		this.load_attendance();
// // 		this.load_leaves();
// // 	}

// // 	// ---------- Employee profile card ----------
// // 	load_employee() {
// // 		frappe.call({
// // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// // 			args: { employee: this.employee },
// // 			callback: (r) => {
// // 				if (r.message) this.render_employee_card(r.message);
// // 			},
// // 		});
// // 	}

// // 	render_employee_card(e) {
// // 		const image = e.image
// // 			? `<img src="${e.image}">`
// // 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// // 		const is_active = e.status === 'Active';

// // 		const detail = (label, value) => `
// // 			<div class="ed-detail-row">
// // 				<div class="ed-detail-label">${label}</div>
// // 				<div class="ed-detail-value" title="${value || ''}">${value || '-'}</div>
// // 			</div>`;

// // 		this.$container.find('.ed-profile-card').html(`
// // 			<div class="ed-profile-header">
// // 				<div class="ed-avatar">${image}</div>
// // 				<div class="ed-profile-main">
// // 					<div class="ed-name-row">
// // 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// // 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// // 					</div>
// // 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// // 					<div class="ed-sub ed-muted">${e.employee}</div>
// // 				</div>
// // 			</div>
// // 			<div class="ed-detail-grid">
// // 				<div class="ed-detail-col">
// // 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// // 					${detail('Gender', e.gender)}
// // 					${detail('Marital Status', e.marital_status)}
// // 					${detail('Blood Group', e.blood_group)}
// // 					${detail('Reports To', e.reports_to)}
// // 				</div>
// // 				<div class="ed-detail-col">
// // 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// // 					${detail('Email', e.company_email)}
// // 					${detail('Phone', e.cell_number)}
// // 					<div class="ed-detail-row">
// // 						<div class="ed-detail-label">Address</div>
// // 						<div class="ed-detail-value ed-detail-value-wrap" title="${e.current_address || ''}">${e.current_address || '-'}</div>
// // 					</div>

// // 				</div>
// // 				<div class="ed-detail-col">
// // 					${detail('Aadhaar No.', e.aadhaar_number)}
// // 					${detail('PAN No.', e.pan_number)}
// // 					${detail('PF No.', e.provident_fund_account)}
// // 					${detail('UAN No.', e.uan)}
// // 					${detail('ESI No.', e.esic_no)}
// // 				</div>
// // 			</div>
// // 		`);
// // 	}

// // 	// ---------- Attendance ----------
// // 	load_attendance() {
// // 		if (!this.employee) return;
// // 		frappe.call({
// // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_payroll_attendance',
// // 			args: { employee: this.employee, year: this.year },
// // 			callback: (r) => {
// // 				if (r.message) this.render_attendance(r.message);
// // 			},
// // 		});
// // 	}

// // 	render_attendance(data) {
// // 		const legend_items = [
// // 			['XX', 'Present', 'att-present'],
// // 			['AA', 'Absent / LOP', 'att-absent'],
// // 			['0.5..', 'Half Day', 'att-halfday'],
// // 			['CL/SL/EL', 'On Leave', 'att-leave'],
// // 			['HH', 'Holiday', 'att-holiday'],
// // 		];
// // 		const legend = `<div class="ed-legend">${legend_items
// // 			.map(([code, label, cls]) => `<span class="ed-legend-item"><span class="att-cell-mini ${cls}">${code}</span>${label}</span>`)
// // 			.join('')}
// // 			<span class="ed-legend-item"><span class="att-cell-mini att-legend-late-swatch"></span>Late Entry</span>
// // 			<span class="ed-legend-item"><span class="att-cell-mini att-legend-permission-swatch"></span>Permission</span>
// // 		</div>`;

// // 		const totals_cells = (t, is_header) => `
// // 			<div class="att-total-cell">${is_header ? 'Cal. Days' : t.calendar_days}</div>
// // 			<div class="att-total-cell">${is_header ? 'Working Days' : t.working_days}</div>
// // 			<div class="att-total-cell">${is_header ? 'Worked Days' : t.worked_days}</div>
// // 			<div class="att-total-cell att-col-ee">${is_header ? 'EE' : (t.ee || '-')}</div>
// // 			<div class="att-total-cell att-col-cc">${is_header ? 'CC' : (t.cc || '-')}</div>
// // 			<div class="att-total-cell att-col-ss">${is_header ? 'SS' : (t.ss || '-')}</div>
// // 			<div class="att-total-cell att-col-splml">${is_header ? 'Spl/ML' : (t.spl_ml || '-')}</div>
// // 			<div class="att-total-cell att-col-wwhh">${is_header ? 'WW/HH' : t.ww_hh}</div>
// // 			<div class="att-total-cell">${is_header ? 'Paid Days' : t.paid_days}</div>
// // 			<div class="att-total-cell att-col-aa">${is_header ? 'AA' : (t.aa || '-')}</div>
// // 			<div class="att-total-cell att-col-late">${is_header ? 'Late' : (t.late || '-')}</div>
// // 			<div class="att-total-cell att-col-permission">${is_header ? 'Permission' : (t.permission || '-')}</div>
// // 		`;

// // 		const MAX_DAYS = 31;
// // 		let rows_html = '';
// // 		data.rows.forEach((row) => {
// // 			let day_cells = row.days
// // 				.map(
// // 					(d) => `
// // 					<div class="att-day-col">
// // 						<div class="att-day-num">${d.day}</div>
// // 						<div class="att-day-code ${d.css}">${d.code || ''}</div>
// // 					</div>`
// // 				)
// // 				.join('');
// // 			// pad shorter months (28-30 days) so totals columns stay aligned across rows
// // 			for (let i = row.days.length; i < MAX_DAYS; i++) {
// // 				day_cells += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// // 			}

// // 			rows_html += `
// // 				<div class="att-row">
// // 					<div class="att-month-label">${row.month_name}</div>
// // 					<div class="att-day-strip">${day_cells}</div>
// // 					<div class="att-totals-cells">${totals_cells(row.totals, false)}</div>
// // 				</div>`;
// // 		});

// // 		// header/grand rows need the SAME day-strip width as data rows (all filler,
// // 		// all invisible) so the totals columns line up vertically underneath them
// // 		let filler_strip = '';
// // 		for (let i = 0; i < MAX_DAYS; i++) {
// // 			filler_strip += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// // 		}

// // 		const header_row = `
// // 			<div class="att-row att-header-row">
// // 				<div class="att-month-label"></div>
// // 				<div class="att-day-strip">${filler_strip}</div>
// // 				<div class="att-totals-cells att-totals-header">${totals_cells(null, true)}</div>
// // 			</div>`;

// // 		const grand_row = `
// // 			<div class="att-row att-grand-row">
// // 				<div class="att-month-label">Total</div>
// // 				<div class="att-day-strip">${filler_strip}</div>
// // 				<div class="att-totals-cells">${totals_cells(data.grand_totals, false)}</div>
// // 			</div>`;

// // 		this.$container.find('.ed-attendance-body').html(`
// // 			${legend}
// // 			<div class="att-table-wrap">
// // 				${header_row}
// // 				${rows_html}
// // 				${grand_row}
// // 			</div>
// // 		`);
// // 	}

// // 	// ---------- Leaves ----------
// // 	load_leaves() {
// // 		if (!this.employee) return;
// // 		frappe.call({
// // 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// // 			args: { employee: this.employee, year: this.year },
// // 			callback: (r) => {
// // 				if (r.message) this.render_leaves(r.message);
// // 			},
// // 		});
// // 	}

// // 	render_leaves(data) {
// // 		let cards = '';
// // 		data.leave_types.forEach((lt) => {
// // 			cards += `
// // 				<div class="ed-leave-tile">
// // 					<div class="ed-leave-tile-title">${lt.leave_type}</div>
// // 					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// // 					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// // 					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// // 				</div>`;
// // 		});
// // 		cards += `
// // 			<div class="ed-leave-tile ed-leave-tile-lop">
// // 				<div class="ed-leave-tile-title">Loss of Pay</div>
// // 				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// // 			</div>`;

// // 		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// // 	}

// // 	// ---------- Styles ----------
// // 	inject_styles() {
// // 		if (document.getElementById('ed-styles')) return;
// // 		$(`<style id="ed-styles">
// // 			.page-content .container,
// // 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// // 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// // 			.ed-wrapper {
// // 				width: 80%;
// // 				max-width: 1400px;
// // 				margin: 0 auto;
// // 				padding: 20px 0 40px;
// // 				box-sizing: border-box;
// // 			}
// // 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// // 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// // 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// // 			@media (max-width: 640px) {
// // 				.page-form .form-group,
// // 				.page-form .frappe-control { width: 100% !important; }
// // 				.page-form { display:flex; flex-direction:column; gap:4px; }
// // 			}

// // 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

// // 			/* ---- card base + per-section color ---- */
// // 			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
// // 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// // 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// // 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
// // 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:16px; }
// //  			.ed-detail-value-wrap {
// //  				white-space: normal !important;
// //  				overflow: visible !important;
// //  				text-overflow: unset !important;
// //  				word-break: break-word;
// //  				line-height: 1.4;
// // 			}
// // 			/* ---- profile card ---- */
// // 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// // 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// // 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
// // 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// // 			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
// // 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
// // 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
// // 			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
// // 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// // 			.ed-muted { color:#94a3b8; }
// // 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// // 			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
// // 			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
// // 			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

// // 			/* ---- attendance: payroll-cycle table ---- */
// // 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// // 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// // 			.att-cell-mini { display:inline-block; min-width:26px; text-align:center; font-size:9px; font-weight:700; border-radius:4px; padding:2px 3px; }
// // 			.att-legend-late-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 -2px 0 0 #dc2626; }
// // 			.att-legend-permission-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 2px 0 0 #2563eb; }

// // 			.att-table-wrap { overflow-x:auto; border-radius:10px; border:1px solid #fed7aa; background:#fff; }
// // 			.att-row { display:flex; align-items:stretch; border-bottom:1px solid #fed7aa; }
// // 			.att-row:last-child { border-bottom:none; }
// // 			.att-month-label { flex:0 0 90px; display:flex; align-items:center; padding:6px 10px; font-size:12px; font-weight:700; color:#9a3412; background:#fff2e0; position:sticky; left:0; z-index:2; }
// // 			.att-day-strip { display:flex; flex:0 0 auto; }
// // 			.att-day-col { flex:0 0 26px; width:26px; text-align:center; border-right:1px solid #fef3e2; }
// // 			.att-day-num { font-size:9px; color:#78716c; padding:3px 0 1px; background:#fffaf0; }
// // 			.att-day-code { font-size:8.5px; font-weight:700; padding:3px 0; min-height:14px; }
// // 			.att-day-filler .att-day-num, .att-day-filler .att-day-code { background:transparent; }
// // 			.att-present { background:#f4f6f8; color:#94a3b8; }
// // 			.att-absent { background:#ef444455; color:#b91c1c; }
// // 			.att-halfday { background:#f59e0b55; color:#b45309; }
// // 			.att-leave { background:#3b82f655; color:#1d4ed8; }
// // 			.att-holiday { background:#a855f755; color:#7e22ce; }
// // 			/* weekly-offs are intentionally NOT highlighted - the "WW" code
// // 			   still shows, just without a colored background */
// // 			.att-weeklyoff { background:transparent; color:#78716c; }
// // 			.att-wfh { background:#14b8a655; color:#0f766e; }
// // 			.att-other { background:#e2e8f0; color:#475569; }
// // 			.att-blank { background:#fff; }
// // 			/* late-entry / permission are overlay flags on top of a day's
// // 			   normal status colour, shown as a thin coloured bar so they
// // 			   don't fight with the status background */
// // 			.att-late-flag { box-shadow: inset 0 -2px 0 0 #dc2626; }
// // 			.att-permission-flag { box-shadow: inset 0 2px 0 0 #2563eb; }

// // 			.att-totals-cells { display:flex; flex:0 0 auto; }
// // 			.att-total-cell { flex:0 0 68px; width:68px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#1e293b; border-right:1px solid #fef3e2; padding:0 4px; text-align:center; }
// // 			.att-totals-header .att-total-cell { font-size:10px; color:#fff; background:#f97316; font-weight:700; padding:8px 4px; }
// // 			.att-col-ee { color:#6366f1; }
// // 			.att-col-cc { color:#f97316; }
// // 			.att-col-ss { color:#14b8a6; }
// // 			.att-col-splml { color:#ec4899; }
// // 			.att-col-wwhh { color:#92600a; }
// // 			.att-col-aa { color:#dc2626; }
// // 			.att-col-late { color:#dc2626; }
// // 			.att-col-permission { color:#2563eb; }
// // 			.att-header-row .att-month-label { background:#fff2e0; }
// // 			.att-grand-row { background:#fff2e0; font-weight:800; }
// // 			.att-grand-row .att-total-cell { font-weight:800; }

// // 			/* ---- leaves ---- */
// // 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
// // 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
// // 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// // 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
// // 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
// // 			.ed-leave-balance b { color:#059669; font-size:14px; }
// // 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

// // 			/* ---- mobile ---- */
// // 			@media (max-width: 640px) {
// // 				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
// // 				.ed-name-row { justify-content: center; }
// // 				.ed-name { font-size: 17px; }
// // 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// // 				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
// // 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// // 				.ed-card { padding: 16px; }
// // 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// // 				.att-day-col { flex-basis: 22px; width: 22px; }
// // 				.att-total-cell { flex-basis: 56px; width: 56px; font-size: 10px; }
// // 				.att-month-label { flex-basis: 70px; font-size: 11px; }
// // 			}
// // 		</style>`).appendTo('head');
// // 	}
// // }




// frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
// 	const page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Employee Dashboard',
// 		single_column: true,
// 	});

// 	new EmployeeDashboard(page);
// };

// class EmployeeDashboard {
// 	constructor(page) {
// 		this.page = page;
// 		this.year = new Date().getFullYear();

// 		// each history section keeps its own independent year filter
// 		this.leavehist_year = new Date().getFullYear();
// 		this.latehist_year = new Date().getFullYear();
// 		this.permission_year = new Date().getFullYear();

// 		this.employee = null;

// 		this.inject_styles();
// 		this.setup_toolbar();
// 		this.render_skeleton();
// 		this.set_default_employee();
// 	}

// 	// ---------- Toolbar (employee picker + year picker) ----------
// 	setup_toolbar() {
// 		this.employee_field = this.page.add_field({
// 			label: 'Employee',
// 			fieldname: 'employee',
// 			fieldtype: 'Link',
// 			options: 'Employee',
// 			change: () => {
// 				const val = this.employee_field.get_value();
// 				if (val) {
// 					this.employee = val;
// 					this.load_all();
// 				}
// 			},
// 		});

// 		const year_options = this.get_year_options();

// 		this.year_field = this.page.add_field({
// 			label: 'Year',
// 			fieldname: 'year',
// 			fieldtype: 'Select',
// 			options: year_options,
// 			default: String(this.year),
// 			change: () => {
// 				this.update_year();
// 			},
// 		});

// 		// fallback: Frappe's df.change callback doesn't always fire reliably
// 		// for Select fields, so also bind directly to the native <select>
// 		this.year_field.$input.on('change', () => {
// 			this.update_year();
// 		});
// 	}

// 	get_year_options() {
// 		const options = [];
// 		const current_year = new Date().getFullYear();
// 		for (let y = current_year; y >= current_year - 5; y--) options.push(String(y));
// 		return options;
// 	}

// 	update_year() {
// 		this.year = cint(this.year_field.get_value());
// 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// 		this.load_attendance();
// 		this.load_leaves();
// 	}

// 	set_default_employee() {
// 		frappe.db
// 			.get_value('Employee', { user_id: frappe.session.user }, 'name')
// 			.then((r) => {
// 				const emp = r && r.message && r.message.name;
// 				if (emp) {
// 					this.employee = emp;
// 					this.employee_field.set_value(emp);
// 				}
// 			});
// 	}

// 	// ---------- Layout ----------
// 	render_skeleton() {
// 		const year_select_html = (section, selected) => {
// 			let opts = '';
// 			this.get_year_options().forEach((y) => {
// 				opts += `<option value="${y}" ${cint(y) === cint(selected) ? 'selected' : ''}>${y}</option>`;
// 			});
// 			return `<select class="ed-history-year-select" data-section="${section}">${opts}</select>`;
// 		};

// 		this.$container = $(`
// 			<div class="ed-wrapper">
// 				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
// 				<div class="ed-card ed-profile-card" style="display:none;"></div>

// 				<!-- Leave History -->
// 				<div class="ed-card ed-history-card ed-leavehist-card" style="display:none;">
// 					<div class="ed-history-header">
// 						<div class="ed-section-title">Leave History</div>
// 						${year_select_html('leavehist', this.leavehist_year)}
// 					</div>
// 					<div class="ed-history-stats">
// 						<div class="ed-stat-box">
// 							<div class="ed-stat-label">Total Leave</div>
// 							<div class="ed-stat-value ed-leavehist-total">0</div>
// 						</div>
// 					</div>
// 					<div class="ed-history-legend">
// 						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#6366f1;"></span>EL</span>
// 						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#22c55e;"></span>CL</span>
// 						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#eab308;"></span>SL</span>
// 						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#ef4444;"></span>LOP</span>
// 					</div>
// 					<div class="ed-leavehist-chart ed-history-chart"></div>
// 				</div>

// 				<!-- Late History -->
// 				<div class="ed-card ed-history-card ed-latehist-card" style="display:none;">
// 					<div class="ed-history-header">
// 						<div class="ed-section-title">Late History</div>
// 						${year_select_html('latehist', this.latehist_year)}
// 					</div>
// 					<div class="ed-history-stats">
// 						<div class="ed-stat-box">
// 							<div class="ed-stat-label">Total Late</div>
// 							<div class="ed-stat-value ed-latehist-total">0</div>
// 						</div>
// 					</div>
// 					<div class="ed-latehist-chart ed-history-chart"></div>
// 				</div>

// 				<!-- Permission -->
// 				<div class="ed-card ed-history-card ed-permission-card" style="display:none;">
// 					<div class="ed-history-header">
// 						<div class="ed-section-title">Permission</div>
// 						${year_select_html('permission', this.permission_year)}
// 					</div>
// 					<div class="ed-history-stats">
// 						<div class="ed-stat-box">
// 							<div class="ed-stat-label">Total Permission</div>
// 							<div class="ed-stat-value ed-permission-total">0</div>
// 						</div>
// 					</div>
// 					<div class="ed-permission-chart ed-history-chart"></div>
// 				</div>

// 				<div class="ed-card ed-attendance-card" style="display:none;">
// 					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
// 					<div class="ed-attendance-body"></div>
// 				</div>
// 				<div class="ed-card ed-leave-card" style="display:none;">
// 					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
// 					<div class="ed-leave-body"></div>
// 				</div>
// 			</div>
// 		`).appendTo(this.page.main);

// 		// year-select handlers for the three independent history sections
// 		this.$container.on('change', '.ed-history-year-select', (e) => {
// 			const $sel = $(e.currentTarget);
// 			const section = $sel.data('section');
// 			const year = cint($sel.val());

// 			if (section === 'leavehist') {
// 				this.leavehist_year = year;
// 				this.load_leave_history();
// 			} else if (section === 'latehist') {
// 				this.latehist_year = year;
// 				this.load_late_history();
// 			} else if (section === 'permission') {
// 				this.permission_year = year;
// 				this.load_permission_history();
// 			}
// 		});
// 	}

// 	load_all() {
// 		this.$container.find('.ed-empty-state').hide();
// 		this.$container
// 			.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card, .ed-history-card')
// 			.show();
// 		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
// 		this.load_employee();
// 		this.load_attendance();
// 		this.load_leaves();
// 		this.load_leave_history();
// 		this.load_late_history();
// 		this.load_permission_history();
// 	}

// 	// ---------- Employee profile card ----------
// 	load_employee() {
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
// 			args: { employee: this.employee },
// 			callback: (r) => {
// 				if (r.message) this.render_employee_card(r.message);
// 			},
// 		});
// 	}

// 	render_employee_card(e) {
// 		const image = e.image
// 			? `<img src="${e.image}">`
// 			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

// 		const is_active = e.status === 'Active';

// 		const detail = (label, value) => `
// 			<div class="ed-detail-row">
// 				<div class="ed-detail-label">${label}</div>
// 				<div class="ed-detail-value" title="${value || ''}">${value || '-'}</div>
// 			</div>`;

// 		this.$container.find('.ed-profile-card').html(`
// 			<div class="ed-profile-header">
// 				<div class="ed-avatar">${image}</div>
// 				<div class="ed-profile-main">
// 					<div class="ed-name-row">
// 						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
// 						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
// 					</div>
// 					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
// 					<div class="ed-sub ed-muted">${e.employee}</div>
// 				</div>
// 			</div>
// 			<div class="ed-detail-grid">
// 				<div class="ed-detail-col">
// 					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
// 					${detail('Gender', e.gender)}
// 					${detail('Marital Status', e.marital_status)}
// 					${detail('Blood Group', e.blood_group)}
// 					${detail('Reports To', e.reports_to)}
// 				</div>
// 				<div class="ed-detail-col">
// 					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
// 					${detail('Email', e.company_email)}
// 					${detail('Phone', e.cell_number)}
// 					<div class="ed-detail-row">
// 						<div class="ed-detail-label">Address</div>
// 						<div class="ed-detail-value ed-detail-value-wrap" title="${e.current_address || ''}">${e.current_address || '-'}</div>
// 					</div>
// 				</div>
// 				<div class="ed-detail-col">
// 					${detail('Aadhaar No.', e.aadhaar_number)}
// 					${detail('PAN No.', e.pan_number)}
// 					${detail('PF No.', e.provident_fund_account)}
// 					${detail('UAN No.', e.uan)}
// 					${detail('ESI No.', e.esic_no)}
// 				</div>
// 			</div>
// 		`);
// 	}

// 	// ---------- Leave History (Jan-Dec, EL/CL/SL/LOP, own year filter) ----------
// 	load_leave_history() {
// 		if (!this.employee) return;
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_history',
// 			args: { employee: this.employee, year: this.leavehist_year },
// 			callback: (r) => {
// 				if (r.message) this.render_leave_history(r.message);
// 			},
// 		});
// 	}

// 	render_leave_history(data) {
// 		this.$container.find('.ed-leavehist-total').text(data.total_leave);

// 		const $chart = this.$container.find('.ed-leavehist-chart').empty();
// 		const chart_el = $('<div></div>').appendTo($chart)[0];

// 		new frappe.Chart(chart_el, {
// 			data: {
// 				labels: data.months.map((m) => m.month_name.substring(0, 3)),
// 				datasets: [
// 					{ name: 'EL', values: data.months.map((m) => m.EL) },
// 					{ name: 'CL', values: data.months.map((m) => m.CL) },
// 					{ name: 'SL', values: data.months.map((m) => m.SL) },
// 					{ name: 'LOP', values: data.months.map((m) => m.LOP) },
// 				],
// 			},
// 			type: 'bar',
// 			height: 240,
// 			barOptions: { stacked: 1, spaceRatio: 0.4 },
// 			colors: ['#6366f1', '#22c55e', '#eab308', '#ef4444'],
// 			axisOptions: { xIsSeries: true },
// 		});
// 	}

// 	// ---------- Late History (Jan-Dec count of late-entry days, own year filter) ----------
// 	load_late_history() {
// 		if (!this.employee) return;
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_late_history',
// 			args: { employee: this.employee, year: this.latehist_year },
// 			callback: (r) => {
// 				if (r.message) this.render_late_history(r.message);
// 			},
// 		});
// 	}

// 	render_late_history(data) {
// 		this.$container.find('.ed-latehist-total').text(data.total_late);

// 		const $chart = this.$container.find('.ed-latehist-chart').empty();
// 		const chart_el = $('<div></div>').appendTo($chart)[0];

// 		new frappe.Chart(chart_el, {
// 			data: {
// 				labels: data.months.map((m) => m.month_name.substring(0, 3)),
// 				datasets: [{ name: 'Late Days', values: data.months.map((m) => m.count) }],
// 			},
// 			type: 'bar',
// 			height: 220,
// 			barOptions: { spaceRatio: 0.4 },
// 			colors: ['#f97316'],
// 			axisOptions: { xIsSeries: true },
// 		});
// 	}

// 	// ---------- Permission (Jan-Dec count, own year filter) ----------
// 	load_permission_history() {
// 		if (!this.employee) return;
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_permission_history',
// 			args: { employee: this.employee, year: this.permission_year },
// 			callback: (r) => {
// 				if (r.message) this.render_permission_history(r.message);
// 			},
// 		});
// 	}

// 	render_permission_history(data) {
// 		this.$container.find('.ed-permission-total').text(data.total_permission);

// 		const $chart = this.$container.find('.ed-permission-chart').empty();
// 		const chart_el = $('<div></div>').appendTo($chart)[0];

// 		new frappe.Chart(chart_el, {
// 			data: {
// 				labels: data.months.map((m) => m.month_name.substring(0, 3)),
// 				datasets: [{ name: 'Permission', values: data.months.map((m) => m.count) }],
// 			},
// 			type: 'bar',
// 			height: 220,
// 			barOptions: { spaceRatio: 0.4 },
// 			colors: ['#3b82f6'],
// 			axisOptions: { xIsSeries: true },
// 		});
// 	}

// 	// ---------- Attendance (payroll cycle table) ----------
// 	load_attendance() {
// 		if (!this.employee) return;
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_payroll_attendance',
// 			args: { employee: this.employee, year: this.year },
// 			callback: (r) => {
// 				if (r.message) this.render_attendance(r.message);
// 			},
// 		});
// 	}

// 	render_attendance(data) {
// 		const legend_items = [
// 			['XX', 'Present', 'att-present'],
// 			['AA', 'Absent / LOP', 'att-absent'],
// 			['0.5..', 'Half Day', 'att-halfday'],
// 			['CL/SL/EL', 'On Leave', 'att-leave'],
// 			['HH', 'Holiday', 'att-holiday'],
// 		];
// 		const legend = `<div class="ed-legend">${legend_items
// 			.map(([code, label, cls]) => `<span class="ed-legend-item"><span class="att-cell-mini ${cls}">${code}</span>${label}</span>`)
// 			.join('')}
// 			<span class="ed-legend-item"><span class="att-cell-mini att-legend-late-swatch"></span>Late Entry</span>
// 			<span class="ed-legend-item"><span class="att-cell-mini att-legend-permission-swatch"></span>Permission</span>
// 		</div>`;

// 		const totals_cells = (t, is_header) => `
// 			<div class="att-total-cell">${is_header ? 'Cal. Days' : t.calendar_days}</div>
// 			<div class="att-total-cell">${is_header ? 'Working Days' : t.working_days}</div>
// 			<div class="att-total-cell">${is_header ? 'Worked Days' : t.worked_days}</div>
// 			<div class="att-total-cell att-col-ee">${is_header ? 'EE' : (t.ee || '-')}</div>
// 			<div class="att-total-cell att-col-cc">${is_header ? 'CC' : (t.cc || '-')}</div>
// 			<div class="att-total-cell att-col-ss">${is_header ? 'SS' : (t.ss || '-')}</div>
// 			<div class="att-total-cell att-col-splml">${is_header ? 'Spl/ML' : (t.spl_ml || '-')}</div>
// 			<div class="att-total-cell att-col-wwhh">${is_header ? 'WW/HH' : t.ww_hh}</div>
// 			<div class="att-total-cell">${is_header ? 'Paid Days' : t.paid_days}</div>
// 			<div class="att-total-cell att-col-aa">${is_header ? 'AA' : (t.aa || '-')}</div>
// 			<div class="att-total-cell att-col-late">${is_header ? 'Late' : (t.late || '-')}</div>
// 			<div class="att-total-cell att-col-permission">${is_header ? 'Permission' : (t.permission || '-')}</div>
// 		`;

// 		const MAX_DAYS = 31;
// 		let rows_html = '';
// 		data.rows.forEach((row) => {
// 			let day_cells = row.days
// 				.map(
// 					(d) => `
// 					<div class="att-day-col">
// 						<div class="att-day-num">${d.day}</div>
// 						<div class="att-day-code ${d.css}">${d.code || ''}</div>
// 					</div>`
// 				)
// 				.join('');
// 			for (let i = row.days.length; i < MAX_DAYS; i++) {
// 				day_cells += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// 			}

// 			rows_html += `
// 				<div class="att-row">
// 					<div class="att-month-label">${row.month_name}</div>
// 					<div class="att-day-strip">${day_cells}</div>
// 					<div class="att-totals-cells">${totals_cells(row.totals, false)}</div>
// 				</div>`;
// 		});

// 		let filler_strip = '';
// 		for (let i = 0; i < MAX_DAYS; i++) {
// 			filler_strip += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
// 		}

// 		const header_row = `
// 			<div class="att-row att-header-row">
// 				<div class="att-month-label"></div>
// 				<div class="att-day-strip">${filler_strip}</div>
// 				<div class="att-totals-cells att-totals-header">${totals_cells(null, true)}</div>
// 			</div>`;

// 		const grand_row = `
// 			<div class="att-row att-grand-row">
// 				<div class="att-month-label">Total</div>
// 				<div class="att-day-strip">${filler_strip}</div>
// 				<div class="att-totals-cells">${totals_cells(data.grand_totals, false)}</div>
// 			</div>`;

// 		this.$container.find('.ed-attendance-body').html(`
// 			${legend}
// 			<div class="att-table-wrap">
// 				${header_row}
// 				${rows_html}
// 				${grand_row}
// 			</div>
// 		`);
// 	}

// 	// ---------- Leaves ----------
// 	load_leaves() {
// 		if (!this.employee) return;
// 		frappe.call({
// 			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
// 			args: { employee: this.employee, year: this.year },
// 			callback: (r) => {
// 				if (r.message) this.render_leaves(r.message);
// 			},
// 		});
// 	}

// 	render_leaves(data) {
// 		let cards = '';
// 		data.leave_types.forEach((lt) => {
// 			cards += `
// 				<div class="ed-leave-tile">
// 					<div class="ed-leave-tile-title">${lt.leave_type}</div>
// 					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
// 					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
// 					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
// 				</div>`;
// 		});
// 		cards += `
// 			<div class="ed-leave-tile ed-leave-tile-lop">
// 				<div class="ed-leave-tile-title">Loss of Pay</div>
// 				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
// 			</div>`;

// 		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
// 	}

// 	// ---------- Styles ----------
// 	inject_styles() {
// 		if (document.getElementById('ed-styles')) return;
// 		$(`<style id="ed-styles">
// 			.page-content .container,
// 			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
// 			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
// 			.ed-wrapper {
// 				width: 80%;
// 				max-width: 1400px;
// 				margin: 0 auto;
// 				padding: 20px 0 40px;
// 				box-sizing: border-box;
// 			}
// 			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
// 			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
// 			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
// 			@media (max-width: 640px) {
// 				.page-form .form-group,
// 				.page-form .frappe-control { width: 100% !important; }
// 				.page-form { display:flex; flex-direction:column; gap:4px; }
// 			}

// 			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

// 			/* ---- card base + per-section color ---- */
// 			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
// 			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
// 			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
// 			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
// 			.ed-history-card { background: #fff; border-left: 4px solid #64748b; }
// 			.ed-leavehist-card { border-left-color: #6366f1; }
// 			.ed-latehist-card { border-left-color: #f97316; }
// 			.ed-permission-card { border-left-color: #3b82f6; }
// 			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:0; }
//  			.ed-detail-value-wrap {
//  				white-space: normal !important;
//  				overflow: visible !important;
//  				text-overflow: unset !important;
//  				word-break: break-word;
//  				line-height: 1.4;
// 			}

// 			/* ---- history sections (Leave History / Late History / Permission) ---- */
// 			.ed-history-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
// 			.ed-history-year-select {
// 				border:1px solid #e2e8f0; border-radius:8px; padding:4px 10px; font-size:12.5px;
// 				font-weight:600; color:#334155; background:#f8fafc;
// 			}
// 			.ed-history-stats { display:flex; gap:14px; margin-bottom:12px; }
// 			.ed-stat-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:10px 18px; text-align:center; min-width:120px; }
// 			.ed-stat-label { font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.3px; }
// 			.ed-stat-value { font-size:20px; font-weight:800; color:#1e293b; margin-top:2px; }
// 			.ed-history-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:10px; font-size:12px; color:#475569; }
// 			.ed-legend-dot { width:10px; height:10px; border-radius:3px; display:inline-block; margin-right:5px; vertical-align:middle; }
// 			.ed-history-chart { margin-bottom:4px; }

// 			/* ---- profile card ---- */
// 			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
// 			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
// 			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
// 			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
// 			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
// 			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
// 			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
// 			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
// 			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
// 			.ed-muted { color:#94a3b8; }
// 			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
// 			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
// 			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
// 			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

// 			/* ---- generic table used by history sections + leave summary ---- */
// 			.ed-table-scroll { overflow-x:auto; border-radius:10px; }
// 			.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
// 			.ed-table th, .ed-table td { padding:8px 10px; border-bottom:1px solid #eef1f4; text-align:center; white-space:nowrap; }
// 			.ed-table th { color:#fff; font-weight:700; background:#64748b; }
// 			.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
// 			.ed-totals-row td { font-weight:800; color:#1e293b; background:#f8fafc; }

// 			/* ---- attendance: payroll-cycle table ---- */
// 			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
// 			.ed-legend-item { display:flex; align-items:center; gap:6px; }
// 			.att-cell-mini { display:inline-block; min-width:26px; text-align:center; font-size:9px; font-weight:700; border-radius:4px; padding:2px 3px; }
// 			.att-legend-late-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 -2px 0 0 #dc2626; }
// 			.att-legend-permission-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 2px 0 0 #2563eb; }

// 			.att-table-wrap { overflow-x:auto; border-radius:10px; border:1px solid #fed7aa; background:#fff; }
// 			.att-row { display:flex; align-items:stretch; border-bottom:1px solid #fed7aa; }
// 			.att-row:last-child { border-bottom:none; }
// 			.att-month-label { flex:0 0 90px; display:flex; align-items:center; padding:6px 10px; font-size:12px; font-weight:700; color:#9a3412; background:#fff2e0; position:sticky; left:0; z-index:2; }
// 			.att-day-strip { display:flex; flex:0 0 auto; }
// 			.att-day-col { flex:0 0 26px; width:26px; text-align:center; border-right:1px solid #fef3e2; }
// 			.att-day-num { font-size:9px; color:#78716c; padding:3px 0 1px; background:#fffaf0; }
// 			.att-day-code { font-size:8.5px; font-weight:700; padding:3px 0; min-height:14px; }
// 			.att-day-filler .att-day-num, .att-day-filler .att-day-code { background:transparent; }
// 			.att-present { background:#f4f6f8; color:#94a3b8; }
// 			.att-absent { background:#ef444455; color:#b91c1c; }
// 			.att-halfday { background:#f59e0b55; color:#b45309; }
// 			.att-leave { background:#3b82f655; color:#1d4ed8; }
// 			.att-holiday { background:#a855f755; color:#7e22ce; }
// 			.att-weeklyoff { background:transparent; color:#78716c; }
// 			.att-wfh { background:#14b8a655; color:#0f766e; }
// 			.att-other { background:#e2e8f0; color:#475569; }
// 			.att-blank { background:#fff; }
// 			.att-late-flag { box-shadow: inset 0 -2px 0 0 #dc2626; }
// 			.att-permission-flag { box-shadow: inset 0 2px 0 0 #2563eb; }

// 			.att-totals-cells { display:flex; flex:0 0 auto; }
// 			.att-total-cell { flex:0 0 68px; width:68px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#1e293b; border-right:1px solid #fef3e2; padding:0 4px; text-align:center; }
// 			.att-totals-header .att-total-cell { font-size:10px; color:#fff; background:#f97316; font-weight:700; padding:8px 4px; }
// 			.att-col-ee { color:#6366f1; }
// 			.att-col-cc { color:#f97316; }
// 			.att-col-ss { color:#14b8a6; }
// 			.att-col-splml { color:#ec4899; }
// 			.att-col-wwhh { color:#92600a; }
// 			.att-col-aa { color:#dc2626; }
// 			.att-col-late { color:#dc2626; }
// 			.att-col-permission { color:#2563eb; }
// 			.att-header-row .att-month-label { background:#fff2e0; }
// 			.att-grand-row { background:#fff2e0; font-weight:800; }
// 			.att-grand-row .att-total-cell { font-weight:800; }

// 			/* ---- leaves ---- */
// 			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
// 			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
// 			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
// 			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
// 			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
// 			.ed-leave-balance b { color:#059669; font-size:14px; }
// 			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

// 			/* ---- mobile ---- */
// 			@media (max-width: 640px) {
// 				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
// 				.ed-name-row { justify-content: center; }
// 				.ed-name { font-size: 17px; }
// 				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
// 				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
// 				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
// 				.ed-card { padding: 16px; }
// 				.ed-legend { gap: 8px 12px; font-size: 11px; }
// 				.att-day-col { flex-basis: 22px; width: 22px; }
// 				.att-total-cell { flex-basis: 56px; width: 56px; font-size: 10px; }
// 				.att-month-label { flex-basis: 70px; font-size: 11px; }
// 				.ed-history-header { flex-direction: column; align-items: flex-start; gap: 8px; }
// 				.ed-history-stats { flex-wrap: wrap; }
// 			}
// 		</style>`).appendTo('head');
// 	}
// }


frappe.pages['employee-dashboard'].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Employee Dashboard',
		single_column: true,
	});

	new EmployeeDashboard(page);
};

class EmployeeDashboard {
	constructor(page) {
		this.page = page;
		this.year = new Date().getFullYear();

		// single shared year filter for the three history graphs
		// (Leave History / Late History / Permission)
		this.history_year = new Date().getFullYear();

		this.employee = null;

		this.inject_styles();
		this.setup_toolbar();
		this.render_skeleton();
		this.set_default_employee();
	}

	// ---------- Toolbar (employee picker + year picker) ----------
	setup_toolbar() {
		this.employee_field = this.page.add_field({
			label: 'Employee',
			fieldname: 'employee',
			fieldtype: 'Link',
			options: 'Employee',
			change: () => {
				const val = this.employee_field.get_value();
				if (val) {
					this.employee = val;
					this.load_all();
				}
			},
		});

		const year_options = this.get_year_options();

		this.year_field = this.page.add_field({
			label: 'Year',
			fieldname: 'year',
			fieldtype: 'Select',
			options: year_options,
			default: String(this.year),
			change: () => {
				this.update_year();
			},
		});

		// fallback: Frappe's df.change callback doesn't always fire reliably
		// for Select fields, so also bind directly to the native <select>
		this.year_field.$input.on('change', () => {
			this.update_year();
		});
	}

	get_year_options() {
		const options = [];
		const current_year = new Date().getFullYear();
		for (let y = current_year; y >= current_year - 5; y--) options.push(String(y));
		return options;
	}

	update_year() {
		this.year = cint(this.year_field.get_value());
		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
		this.load_attendance();
		this.load_leaves();
	}

	set_default_employee() {
		frappe.db
			.get_value('Employee', { user_id: frappe.session.user }, 'name')
			.then((r) => {
				const emp = r && r.message && r.message.name;
				if (emp) {
					this.employee = emp;
					this.employee_field.set_value(emp);
				}
			});
	}

	// ---------- Layout ----------
	render_skeleton() {
		const year_select_html = (section, selected) => {
			let opts = '';
			this.get_year_options().forEach((y) => {
				opts += `<option value="${y}" ${cint(y) === cint(selected) ? 'selected' : ''}>${y}</option>`;
			});
			return `<select class="ed-history-year-select" data-section="${section}">${opts}</select>`;
		};

		this.$container = $(`
			<div class="ed-wrapper">
				<div class="ed-empty-state">Select an employee above to view their dashboard.</div>
				<div class="ed-card ed-profile-card" style="display:none;"></div>

				<!-- History: Leave / Late / Permission, one shared year filter -->
				<div class="ed-card ed-history-card" style="display:none;">
					<div class="ed-history-header">
						<div class="ed-section-title">History</div>
						${year_select_html('history', this.history_year)}
					</div>

					<!-- summary row: 3 total boxes side by side -->
					<div class="ed-history-stats-row">
						<div class="ed-stat-box">
							<div class="ed-stat-label">Total Leave</div>
							<div class="ed-stat-value ed-leavehist-total">0</div>
						</div>
						<div class="ed-stat-box">
							<div class="ed-stat-label">Total Late</div>
							<div class="ed-stat-value ed-latehist-total">0</div>
						</div>
						<div class="ed-stat-box">
							<div class="ed-stat-label">Total Permission</div>
							<div class="ed-stat-value ed-permission-total">0</div>
						</div>
					</div>

					<div class="ed-history-subsection-title ed-history-subsection-title-first">Leave History</div>
					<div class="ed-history-legend">
						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#6366f1;"></span>EL</span>
						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#22c55e;"></span>CL</span>
						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#eab308;"></span>SL</span>
						<span class="ed-legend-item"><span class="ed-legend-dot" style="background:#ef4444;"></span>LOP</span>
					</div>
					<div class="ed-leavehist-chart ed-history-chart"></div>

					<div class="ed-history-subsection-title">Late History</div>
					<div class="ed-latehist-chart ed-history-chart"></div>

					<div class="ed-history-subsection-title">Permission</div>
					<div class="ed-permission-chart ed-history-chart"></div>
				</div>

				<div class="ed-card ed-attendance-card" style="display:none;">
					<div class="ed-section-title">Attendance — <span class="ed-year-label"></span></div>
					<div class="ed-attendance-body"></div>
				</div>
				<div class="ed-card ed-leave-card" style="display:none;">
					<div class="ed-section-title">Leave Summary — <span class="ed-year-label-2"></span></div>
					<div class="ed-leave-body"></div>
				</div>
			</div>
		`).appendTo(this.page.main);

		// single shared year filter drives all three history graphs
		this.$container.on('change', '.ed-history-year-select', (e) => {
			this.history_year = cint($(e.currentTarget).val());
			this.load_leave_history();
			this.load_late_history();
			this.load_permission_history();
		});
	}

	load_all() {
		this.$container.find('.ed-empty-state').hide();
		this.$container
			.find('.ed-profile-card, .ed-attendance-card, .ed-leave-card, .ed-history-card')
			.show();
		this.$container.find('.ed-year-label, .ed-year-label-2').text(this.year);
		this.load_employee();
		this.load_attendance();
		this.load_leaves();
		this.load_leave_history();
		this.load_late_history();
		this.load_permission_history();
	}

	// ---------- Employee profile card ----------
	load_employee() {
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_employee_details',
			args: { employee: this.employee },
			callback: (r) => {
				if (r.message) this.render_employee_card(r.message);
			},
		});
	}

	render_employee_card(e) {
		const image = e.image
			? `<img src="${e.image}">`
			: `<div class="ed-avatar-fallback">${frappe.get_abbr(e.employee_name)}</div>`;

		const is_active = e.status === 'Active';

		const detail = (label, value) => `
			<div class="ed-detail-row">
				<div class="ed-detail-label">${label}</div>
				<div class="ed-detail-value" title="${value || ''}">${value || '-'}</div>
			</div>`;

		this.$container.find('.ed-profile-card').html(`
			<div class="ed-profile-header">
				<div class="ed-avatar">${image}</div>
				<div class="ed-profile-main">
					<div class="ed-name-row">
						<span class="ed-name">${frappe.utils.escape_html(e.employee_name || '')}</span>
						<span class="ed-status-pill ${is_active ? 'ed-pill-active' : 'ed-pill-inactive'}">${e.status || ''}</span>
					</div>
					<div class="ed-sub">${e.designation || ''} ${e.department ? '· ' + e.department : ''}</div>
					<div class="ed-sub ed-muted">${e.employee}</div>
				</div>
			</div>
			<div class="ed-detail-grid">
				<div class="ed-detail-col">
					${detail('Date of Birth', frappe.datetime.str_to_user(e.date_of_birth))}
					${detail('Gender', e.gender)}
					${detail('Marital Status', e.marital_status)}
					${detail('Blood Group', e.blood_group)}
					${detail('Reports To', e.reports_to)}
				</div>
				<div class="ed-detail-col">
					${detail('Date of Joining', frappe.datetime.str_to_user(e.date_of_joining))}
					${detail('Email', e.company_email)}
					${detail('Phone', e.cell_number)}
					<div class="ed-detail-row">
						<div class="ed-detail-label">Address</div>
						<div class="ed-detail-value ed-detail-value-wrap" title="${e.current_address || ''}">${e.current_address || '-'}</div>
					</div>
				</div>
				<div class="ed-detail-col">
					${detail('Aadhaar No.', e.aadhaar_number)}
					${detail('PAN No.', e.pan_number)}
					${detail('PF No.', e.provident_fund_account)}
					${detail('UAN No.', e.uan)}
					${detail('ESI No.', e.esic_no)}
				</div>
			</div>
		`);
	}

	// ---------- Leave History (Jan-Dec, EL/CL/SL/LOP, own year filter) ----------
	load_leave_history() {
		if (!this.employee) return;
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_history',
			args: { employee: this.employee, year: this.history_year },
			callback: (r) => {
				if (r.message) this.render_leave_history(r.message);
			},
		});
	}

	render_leave_history(data) {
		this.$container.find('.ed-leavehist-total').text(data.total_leave);

		const $chart = this.$container.find('.ed-leavehist-chart').empty();
		const chart_el = $('<div style="width:100%;"></div>').appendTo($chart)[0];

		new frappe.Chart(chart_el, {
			data: {
				labels: data.months.map((m) => m.month_name.substring(0, 3)),
				datasets: [
					{ name: 'EL', values: data.months.map((m) => m.EL) },
					{ name: 'CL', values: data.months.map((m) => m.CL) },
					{ name: 'SL', values: data.months.map((m) => m.SL) },
					{ name: 'LOP', values: data.months.map((m) => m.LOP) },
				],
			},
			type: 'bar',
			height: 240,
			barOptions: { stacked: 1, spaceRatio: 0.4 },
			colors: ['#6366f1', '#22c55e', '#eab308', '#ef4444'],
			axisOptions: { xIsSeries: true },
		});
	}

	// ---------- Late History (Jan-Dec count of late-entry days, own year filter) ----------
	load_late_history() {
		if (!this.employee) return;
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_late_history',
			args: { employee: this.employee, year: this.history_year },
			callback: (r) => {
				if (r.message) this.render_late_history(r.message);
			},
		});
	}

	render_late_history(data) {
		this.$container.find('.ed-latehist-total').text(data.total_late);

		const $chart = this.$container.find('.ed-latehist-chart').empty();
		const chart_el = $('<div style="width:100%;"></div>').appendTo($chart)[0];

		new frappe.Chart(chart_el, {
			data: {
				labels: data.months.map((m) => m.month_name.substring(0, 3)),
				datasets: [{ name: 'Late Days', values: data.months.map((m) => m.count) }],
			},
			type: 'bar',
			height: 220,
			barOptions: { spaceRatio: 0.4 },
			colors: ['#f97316'],
			axisOptions: { xIsSeries: true },
		});
	}

	// ---------- Permission (Jan-Dec count, own year filter) ----------
	load_permission_history() {
		if (!this.employee) return;
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_permission_history',
			args: { employee: this.employee, year: this.history_year },
			callback: (r) => {
				if (r.message) this.render_permission_history(r.message);
			},
		});
	}

	render_permission_history(data) {
		this.$container.find('.ed-permission-total').text(data.total_permission);

		const $chart = this.$container.find('.ed-permission-chart').empty();
		const chart_el = $('<div style="width:100%;"></div>').appendTo($chart)[0];

		new frappe.Chart(chart_el, {
			data: {
				labels: data.months.map((m) => m.month_name.substring(0, 3)),
				datasets: [{ name: 'Permission', values: data.months.map((m) => m.count) }],
			},
			type: 'bar',
			height: 220,
			barOptions: { spaceRatio: 0.4 },
			colors: ['#3b82f6'],
			axisOptions: { xIsSeries: true },
		});
	}

	// ---------- Attendance (payroll cycle table) ----------
	load_attendance() {
		if (!this.employee) return;
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_payroll_attendance',
			args: { employee: this.employee, year: this.year },
			callback: (r) => {
				if (r.message) this.render_attendance(r.message);
			},
		});
	}

	render_attendance(data) {
		const legend_items = [
			['XX', 'Present', 'att-present'],
			['AA', 'Absent / LOP', 'att-absent'],
			['0.5..', 'Half Day', 'att-halfday'],
			['CL/SL/EL', 'On Leave', 'att-leave'],
			['HH', 'Holiday', 'att-holiday'],
		];
		const legend = `<div class="ed-legend">${legend_items
			.map(([code, label, cls]) => `<span class="ed-legend-item"><span class="att-cell-mini ${cls}">${code}</span>${label}</span>`)
			.join('')}
			<span class="ed-legend-item"><span class="att-cell-mini att-legend-late-swatch"></span>Late Entry</span>
			<span class="ed-legend-item"><span class="att-cell-mini att-legend-permission-swatch"></span>Permission</span>
		</div>`;

		const totals_cells = (t, is_header) => `
			<div class="att-total-cell">${is_header ? 'Cal. Days' : t.calendar_days}</div>
			<div class="att-total-cell">${is_header ? 'Working Days' : t.working_days}</div>
			<div class="att-total-cell">${is_header ? 'Worked Days' : t.worked_days}</div>
			<div class="att-total-cell att-col-ee">${is_header ? 'EE' : (t.ee || '-')}</div>
			<div class="att-total-cell att-col-cc">${is_header ? 'CC' : (t.cc || '-')}</div>
			<div class="att-total-cell att-col-ss">${is_header ? 'SS' : (t.ss || '-')}</div>
			<div class="att-total-cell att-col-splml">${is_header ? 'Spl/ML' : (t.spl_ml || '-')}</div>
			<div class="att-total-cell att-col-wwhh">${is_header ? 'WW/HH' : t.ww_hh}</div>
			<div class="att-total-cell">${is_header ? 'Paid Days' : t.paid_days}</div>
			<div class="att-total-cell att-col-aa">${is_header ? 'AA' : (t.aa || '-')}</div>
			<div class="att-total-cell att-col-late">${is_header ? 'Late' : (t.late || '-')}</div>
			<div class="att-total-cell att-col-permission">${is_header ? 'Permission' : (t.permission || '-')}</div>
		`;

		const MAX_DAYS = 31;
		let rows_html = '';
		data.rows.forEach((row) => {
			let day_cells = row.days
				.map(
					(d) => `
					<div class="att-day-col">
						<div class="att-day-num">${d.day}</div>
						<div class="att-day-code ${d.css}">${d.code || ''}</div>
					</div>`
				)
				.join('');
			for (let i = row.days.length; i < MAX_DAYS; i++) {
				day_cells += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
			}

			rows_html += `
				<div class="att-row">
					<div class="att-month-label">${row.month_name}</div>
					<div class="att-day-strip">${day_cells}</div>
					<div class="att-totals-cells">${totals_cells(row.totals, false)}</div>
				</div>`;
		});

		let filler_strip = '';
		for (let i = 0; i < MAX_DAYS; i++) {
			filler_strip += `<div class="att-day-col att-day-filler"><div class="att-day-num">&nbsp;</div><div class="att-day-code">&nbsp;</div></div>`;
		}

		const header_row = `
			<div class="att-row att-header-row">
				<div class="att-month-label"></div>
				<div class="att-day-strip">${filler_strip}</div>
				<div class="att-totals-cells att-totals-header">${totals_cells(null, true)}</div>
			</div>`;

		const grand_row = `
			<div class="att-row att-grand-row">
				<div class="att-month-label">Total</div>
				<div class="att-day-strip">${filler_strip}</div>
				<div class="att-totals-cells">${totals_cells(data.grand_totals, false)}</div>
			</div>`;

		this.$container.find('.ed-attendance-body').html(`
			${legend}
			<div class="att-table-wrap">
				${header_row}
				${rows_html}
				${grand_row}
			</div>
		`);
	}

	// ---------- Leaves ----------
	load_leaves() {
		if (!this.employee) return;
		frappe.call({
			method: 'infac.infac.page.employee_dashboard.employee_dashboard.get_leave_summary',
			args: { employee: this.employee, year: this.year },
			callback: (r) => {
				if (r.message) this.render_leaves(r.message);
			},
		});
	}

	render_leaves(data) {
		let cards = '';
		data.leave_types.forEach((lt) => {
			cards += `
				<div class="ed-leave-tile">
					<div class="ed-leave-tile-title">${lt.leave_type}</div>
					<div class="ed-leave-tile-row"><span>Allocated</span><b>${lt.allocated}</b></div>
					<div class="ed-leave-tile-row"><span>Taken</span><b>${lt.taken}</b></div>
					<div class="ed-leave-tile-row ed-leave-balance"><span>Balance</span><b>${lt.balance}</b></div>
				</div>`;
		});
		cards += `
			<div class="ed-leave-tile ed-leave-tile-lop">
				<div class="ed-leave-tile-title">Loss of Pay</div>
				<div class="ed-leave-tile-row ed-leave-balance"><span>Days</span><b>${data.loss_of_pay}</b></div>
			</div>`;

		this.$container.find('.ed-leave-body').html(`<div class="ed-leave-grid">${cards}</div>`);
	}

	// ---------- Styles ----------
	inject_styles() {
		if (document.getElementById('ed-styles')) return;
		$(`<style id="ed-styles">
			.page-content .container,
			.page-content .container-fluid { max-width: 100% !important; width: 100% !important; }
			.page-content-wrapper { display: flex; justify-content: center; background: #f4f6fb; }
			.ed-wrapper {
				width: 80%;
				max-width: 1400px;
				margin: 0 auto;
				padding: 20px 0 40px;
				box-sizing: border-box;
			}
			@media (max-width: 1400px) { .ed-wrapper { width: 75%; } }
			@media (max-width: 1100px) { .ed-wrapper { width: 90%; } }
			@media (max-width: 768px) { .ed-wrapper { width: 100%; padding: 12px 12px 40px; } }
			@media (max-width: 640px) {
				.page-form .form-group,
				.page-form .frappe-control { width: 100% !important; }
				.page-form { display:flex; flex-direction:column; gap:4px; }
			}

			.ed-empty-state { text-align:center; color:#8d99a6; padding: 60px 0; font-size: 14px; }

			/* ---- card base + per-section color ---- */
			.ed-card { background:#fff; border-radius:14px; padding:20px 24px; margin-bottom:20px; box-shadow: 0 2px 10px rgba(20,30,60,0.05); border:1px solid #e3e8ee; }
			.ed-profile-card { background: #eef2ff; border-color: #c7d2fe; border-left: 4px solid #6366f1; }
			.ed-attendance-card { background: #fff7ed; border-color: #fed7aa; border-left: 4px solid #f97316; }
			.ed-leave-card { background: #ecfdf5; border-color: #a7f3d0; border-left: 4px solid #10b981; }
			.ed-history-card { background: #fff; border-left: 4px solid #64748b; }
			.ed-leavehist-card { border-left-color: #6366f1; }
			.ed-latehist-card { border-left-color: #f97316; }
			.ed-permission-card { border-left-color: #3b82f6; }
			.ed-section-title { font-size:15px; font-weight:700; color:#1e293b; margin-bottom:0; }
 			.ed-detail-value-wrap {
 				white-space: normal !important;
 				overflow: visible !important;
 				text-overflow: unset !important;
 				word-break: break-word;
 				line-height: 1.4;
			}

			/* ---- history sections (Leave History / Late History / Permission) ---- */
			.ed-history-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
			.ed-history-year-select {
				border:1px solid #e2e8f0; border-radius:8px; padding:4px 10px; font-size:12.5px;
				font-weight:600; color:#334155; background:#f8fafc;
			}
			.ed-history-stats-row { display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin-bottom:18px; }
			.ed-stat-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:14px 18px; text-align:center; }
			.ed-stat-label { font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.3px; }
			.ed-stat-value { font-size:22px; font-weight:800; color:#1e293b; margin-top:4px; }
			.ed-history-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:10px; font-size:12px; color:#475569; }
			.ed-legend-dot { width:10px; height:10px; border-radius:3px; display:inline-block; margin-right:5px; vertical-align:middle; }
			.ed-history-chart { width:100%; min-height:220px; margin-bottom:4px; }
			.ed-history-subsection-title { font-size:14px; font-weight:700; color:#1e293b; margin:22px 0 12px; padding-top:18px; border-top:1px solid #eef1f4; }
			.ed-history-subsection-title-first { margin-top:0; padding-top:0; border-top:none; }

			/* ---- profile card ---- */
			.ed-profile-header { display:flex; align-items:center; gap:18px; padding-bottom:16px; border-bottom:1px solid rgba(99,102,241,0.15); margin-bottom:16px; }
			.ed-avatar img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
			.ed-avatar-fallback { width:64px; height:64px; border-radius:50%; background:#6366f1; color:#fff; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; }
			.ed-name-row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
			.ed-name { font-size:18px; font-weight:800; color:#1e293b; }
			.ed-status-pill { font-size:11px; font-weight:700; padding:3px 12px; border-radius:20px; }
			.ed-pill-active { background:#22c55e; color:#fff; box-shadow: 0 2px 6px rgba(34,197,94,0.4); }
			.ed-pill-inactive { background:#f97316; color:#fff; box-shadow: 0 2px 6px rgba(249,115,22,0.4); }
			.ed-sub { font-size:13px; color:#475569; margin-top:2px; }
			.ed-muted { color:#94a3b8; }
			.ed-detail-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 24px; }
			.ed-detail-row { display:flex; align-items:baseline; justify-content:space-between; padding:7px 0; border-bottom:1px dashed #e2e8f0; font-size:13px; gap:16px; }
			.ed-detail-label { color:#64748b; flex:0 0 auto; white-space:nowrap; }
			.ed-detail-value { color:#1e293b; font-weight:400; text-align:right; flex:1 1 auto; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

			/* ---- generic table used by history sections + leave summary ---- */
			.ed-table-scroll { overflow-x:auto; border-radius:10px; }
			.ed-table { width:100%; border-collapse:collapse; font-size:12.5px; }
			.ed-table th, .ed-table td { padding:8px 10px; border-bottom:1px solid #eef1f4; text-align:center; white-space:nowrap; }
			.ed-table th { color:#fff; font-weight:700; background:#64748b; }
			.ed-table td:first-child, .ed-table th:first-child { text-align:left; }
			.ed-totals-row td { font-weight:800; color:#1e293b; background:#f8fafc; }

			/* ---- attendance: payroll-cycle table ---- */
			.ed-legend { display:flex; flex-wrap:wrap; gap:14px; margin-bottom:16px; font-size:12px; color:#5c6b7a; }
			.ed-legend-item { display:flex; align-items:center; gap:6px; }
			.att-cell-mini { display:inline-block; min-width:26px; text-align:center; font-size:9px; font-weight:700; border-radius:4px; padding:2px 3px; }
			.att-legend-late-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 -2px 0 0 #dc2626; }
			.att-legend-permission-swatch { background:#fff; border:1px solid #e2e8f0; box-shadow: inset 0 2px 0 0 #2563eb; }

			.att-table-wrap { overflow-x:auto; border-radius:10px; border:1px solid #fed7aa; background:#fff; }
			.att-row { display:flex; align-items:stretch; border-bottom:1px solid #fed7aa; }
			.att-row:last-child { border-bottom:none; }
			.att-month-label { flex:0 0 90px; display:flex; align-items:center; padding:6px 10px; font-size:12px; font-weight:700; color:#9a3412; background:#fff2e0; position:sticky; left:0; z-index:2; }
			.att-day-strip { display:flex; flex:0 0 auto; }
			.att-day-col { flex:0 0 26px; width:26px; text-align:center; border-right:1px solid #fef3e2; }
			.att-day-num { font-size:9px; color:#78716c; padding:3px 0 1px; background:#fffaf0; }
			.att-day-code { font-size:8.5px; font-weight:700; padding:3px 0; min-height:14px; }
			.att-day-filler .att-day-num, .att-day-filler .att-day-code { background:transparent; }
			.att-present { background:#f4f6f8; color:#94a3b8; }
			.att-absent { background:#ef444455; color:#b91c1c; }
			.att-halfday { background:#f59e0b55; color:#b45309; }
			.att-leave { background:#3b82f655; color:#1d4ed8; }
			.att-holiday { background:#a855f755; color:#7e22ce; }
			.att-weeklyoff { background:transparent; color:#78716c; }
			.att-wfh { background:#14b8a655; color:#0f766e; }
			.att-other { background:#e2e8f0; color:#475569; }
			.att-blank { background:#fff; }
			.att-late-flag { box-shadow: inset 0 -2px 0 0 #dc2626; }
			.att-permission-flag { box-shadow: inset 0 2px 0 0 #2563eb; }

			.att-totals-cells { display:flex; flex:0 0 auto; }
			.att-total-cell { flex:0 0 68px; width:68px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#1e293b; border-right:1px solid #fef3e2; padding:0 4px; text-align:center; }
			.att-totals-header .att-total-cell { font-size:10px; color:#fff; background:#f97316; font-weight:700; padding:8px 4px; }
			.att-col-ee { color:#6366f1; }
			.att-col-cc { color:#f97316; }
			.att-col-ss { color:#14b8a6; }
			.att-col-splml { color:#ec4899; }
			.att-col-wwhh { color:#92600a; }
			.att-col-aa { color:#dc2626; }
			.att-col-late { color:#dc2626; }
			.att-col-permission { color:#2563eb; }
			.att-header-row .att-month-label { background:#fff2e0; }
			.att-grand-row { background:#fff2e0; font-weight:800; }
			.att-grand-row .att-total-cell { font-weight:800; }

			/* ---- leaves ---- */
			.ed-leave-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:14px; }
			.ed-leave-tile { border:1px solid #a7f3d0; border-radius:10px; padding:16px; background:#fff; }
			.ed-leave-tile-lop { background:#fef2f2; border-color:#fecaca; }
			.ed-leave-tile-title { font-size:13px; font-weight:700; color:#065f46; margin-bottom:10px; }
			.ed-leave-tile-row { display:flex; justify-content:space-between; font-size:12px; color:#475569; padding:3px 0; }
			.ed-leave-balance b { color:#059669; font-size:14px; }
			.ed-leave-tile-lop .ed-leave-balance b { color:#dc2626; }

			/* ---- mobile ---- */
			@media (max-width: 640px) {
				.ed-profile-header { flex-direction: column; text-align: center; gap: 10px; }
				.ed-name-row { justify-content: center; }
				.ed-name { font-size: 17px; }
				.ed-avatar img, .ed-avatar-fallback { width: 60px; height: 60px; }
				.ed-detail-grid { grid-template-columns: 1fr; gap: 0; }
				.ed-detail-col:not(:last-child) { border-bottom: 1px solid #eef1f4; padding-bottom: 8px; margin-bottom: 8px; }
				.ed-card { padding: 16px; }
				.ed-legend { gap: 8px 12px; font-size: 11px; }
				.att-day-col { flex-basis: 22px; width: 22px; }
				.att-total-cell { flex-basis: 56px; width: 56px; font-size: 10px; }
				.att-month-label { flex-basis: 70px; font-size: 11px; }
				.ed-history-header { flex-direction: column; align-items: flex-start; gap: 8px; }
				.ed-history-stats-row { grid-template-columns: 1fr; }
			}
		</style>`).appendTo('head');
	}
}