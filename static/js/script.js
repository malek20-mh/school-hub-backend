document.addEventListener('DOMContentLoaded', function() {
    
    // إزالة التأثيرات عند الخروج (تنظيف)
    const cards = document.querySelectorAll('.card-3d');
    cards.forEach(card => {
        card.removeEventListener('mousemove', function(){});
        card.removeEventListener('mouseleave', function(){});
    });

    // كود حفظ صورة المجموعة (Screenshot)
    const saveButtons = document.querySelectorAll('.btn-save-group');

    if (saveButtons.length > 0) {
        saveButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation(); 
                
                const targetId = this.getAttribute('data-target-id');
                const elementToSave = document.getElementById(targetId);
                
                if (!elementToSave) {
                    console.error('لم يتم العثور على العنصر: ' + targetId);
                    return;
                }

                const originalButtonText = this.textContent;
                this.textContent = '...جاري التحضير';
                
                // التأكد من تحميل مكتبة html2canvas قبل الاستخدام
                if (typeof html2canvas !== 'undefined') {
                    html2canvas(elementToSave, {
                        backgroundColor: "#131201", 
                        scale: 2, 
                        useCORS: true 
                    }).then(canvas => {
                        const leagueName = document.querySelector('.league-logo-container h2')?.textContent.trim() || 'league';
                        
                        // محاولة جلب اسم المجموعة
                        const groupHeader = elementToSave.previousElementSibling; 
                        let groupName = 'group';
                        if (groupHeader && groupHeader.classList.contains('group-header') && groupHeader.querySelector('h3')) {
                                groupName = groupHeader.querySelector('h3').textContent.trim();
                        }

                        const link = document.createElement('a');
                        link.download = `standings-${leagueName}-${groupName}.png`;
                        link.href = canvas.toDataURL('image/png');
                        
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);

                        this.textContent = originalButtonText; 

                    }).catch(err => {
                        console.error('html2canvas error:', err);
                        this.textContent = '❌ فشل';
                        setTimeout(() => { this.textContent = originalButtonText; }, 3000);
                    });
                } else {
                    alert('مكتبة تحويل الصور غير محملة، تأكد من الاتصال بالإنترنت.');
                    this.textContent = originalButtonText;
                }
            });
        });
    }
    // ... الكود السابق ...

    // ⚡ كود حفظ قائمة الهدافين (Scorers)
    const downloadScorersBtn = document.getElementById('download-scorers-btn');
    const scorersCard = document.getElementById('scorers-card-to-save');

    if (downloadScorersBtn && scorersCard) {
        downloadScorersBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const originalButtonText = this.textContent;
            this.textContent = '...جاري التحضير';
            
            if (typeof html2canvas !== 'undefined') {
                html2canvas(scorersCard, {
                    backgroundColor: "#131201",
                    scale: 2,
                    useCORS: true
                }).then(canvas => {
                    // محاولة جلب اسم الدوري من العنوان
                    const leagueTitle = scorersCard.querySelector('h2');
                    let fileName = 'scorers-list';
                    if(leagueTitle) fileName += '-' + leagueTitle.textContent.trim();

                    const link = document.createElement('a');
                    link.download = `${fileName}.png`;
                    link.href = canvas.toDataURL('image/png');
                    
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    this.textContent = originalButtonText;

                }).catch(err => {
                    console.error('html2canvas error:', err);
                    this.textContent = '❌ فشل';
                    setTimeout(() => { this.textContent = originalButtonText; }, 3000);
                });
            }
        });
    }
    // ... الأكواد السابقة ...

    // ⚡ كود حفظ بطاقة المباراة (Match Card)
    const downloadMatchBtn = document.getElementById('download-match-card-btn');
    const matchCard = document.getElementById('match-card-to-save');

    if (downloadMatchBtn && matchCard) {
        downloadMatchBtn.addEventListener('click', function() {
            
            const originalButtonText = this.textContent;
            this.textContent = '...جاري التحضير';

            if (typeof html2canvas !== 'undefined') {
                html2canvas(matchCard, {
                    backgroundColor: "#131201",
                    scale: 2,
                    useCORS: true
                }).then(canvas => {
                    
                    // محاولة إنشاء اسم ملف ذكي
                    const teamA = matchCard.querySelectorAll('.team-info h2')[0]?.textContent.trim() || 'TeamA';
                    const teamB = matchCard.querySelectorAll('.team-info h2')[1]?.textContent.trim() || 'TeamB';
                    
                    const link = document.createElement('a');
                    link.download = `match-card-${teamA}-vs-${teamB}.png`;
                    link.href = canvas.toDataURL('image/png');
                    
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    this.textContent = originalButtonText;
                    
                }).catch(err => {
                    console.error('html2canvas error:', err);
                    this.textContent = '❌ فشل';
                    setTimeout(() => { this.textContent = originalButtonText; }, 3000);
                });
            }
        });
    }
    // ... الأكواد السابقة ...

    // ⚡ كود حفظ جدول المباريات (Schedule Export)
    const downloadScheduleBtn = document.getElementById('download-schedule-btn');
    const scheduleContainer = document.getElementById('schedule-to-capture');

    if (downloadScheduleBtn && scheduleContainer) {
        downloadScheduleBtn.addEventListener('click', function() {
            const btn = this;
            const originalText = btn.textContent;
            btn.textContent = '...جاري التحضير';
            
            if (typeof html2canvas !== 'undefined') {
                html2canvas(scheduleContainer, {
                    scale: 3, // جودة عالية
                    backgroundColor: "#000000",
                    useCORS: true
                }).then(canvas => {
                    // جلب اسم الدوري من الصفحة ليكون اسم الملف
                    const leagueNameEl = scheduleContainer.querySelector('.league-name-sub');
                    const leagueName = leagueNameEl ? leagueNameEl.textContent.trim() : 'league';

                    const link = document.createElement('a');
                    link.download = `matches-schedule-${leagueName}.png`;
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                    
                    btn.textContent = originalText;
                }).catch(err => {
                    console.error('Failed to capture image:', err);
                    btn.textContent = '❌ فشل الحفظ';
                    setTimeout(() => { btn.textContent = originalText; }, 3000);
                });
            } else {
                alert('مكتبة التصوير غير جاهزة، يرجى تحديث الصفحة.');
                btn.textContent = originalText;
            }
        });
    }
    // ... الأكواد السابقة ...

    // ⚡ تأثيرات حقول النماذج (إضافة كلاس للأب عند التركيز)
    const formInputs = document.querySelectorAll('.modern-form input, .modern-form select, .modern-form textarea');
    
    formInputs.forEach(input => {
        // إضافة تغليف للحقل لإظهار الأيقونة (اختياري، يعتمد على الـ HTML)
        if (!input.parentElement.classList.contains('icon-field-wrapper')) {
            // يمكن هنا إضافة كلاس للأب لتنسيق الأيقونات إذا لزم الأمر
            input.parentElement.classList.add('input-group-styled');
        }

        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.01)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    });
    // ... الأكواد السابقة ...

    // ⚡ إدارة القوائم المنسدلة المخصصة (Custom Dropdowns)
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation(); // منع إغلاق القائمة فوراً
            const menu = this.nextElementSibling;
            if (menu) {
                // إغلاق أي قائمة أخرى مفتوحة
                document.querySelectorAll('.dropdown-menu').forEach(m => {
                    if (m !== menu) m.style.display = 'none';
                });
                
                // تبديل حالة القائمة الحالية
                menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
            }
        });
    });

    // إغلاق القوائم عند النقر في أي مكان آخر
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.dropdown-toggle')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    // ⚡ تأثيرات صفوف الجداول (Hover Effects)
    const hoverRows = document.querySelectorAll('.table-row, .cyan-table tbody tr');
    hoverRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'translateX(5px)';
            row.style.transition = 'transform 0.3s ease';
        });
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'translateX(0)';
        });
    });
    document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 🔔 1. نظام الإشعارات (Notifications System)
    // ============================================================
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationList = document.getElementById('notificationList');
    const badgeElement = document.getElementById('notificationBadge');

    // دالة مساعدة لجلب CSRF Token (مهمة جداً لطلبات POST في Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // دالة جلب الإشعارات من السيرفر
    async function fetchNotifications() {
        if (!notificationBtn) return; // إذا لم يكن الزر موجوداً (غير مسجل دخول)
        
        try {
            const response = await fetch('/api/notifications/');
            if (response.ok) {
                const data = await response.json();
                updateNotificationUI(data);
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }

    // دالة تحديث الواجهة (HTML) بناءً على البيانات
    function updateNotificationUI(notifications) {
        if (!notificationList || !badgeElement) return;

        const unreadCount = notifications.filter(n => !n.is_read).length;

        // تحديث العداد الأحمر
        if (unreadCount > 0) {
            badgeElement.textContent = unreadCount;
            badgeElement.style.display = 'block';
            badgeElement.style.animation = 'bounce 0.5s ease'; // تأثير حركي
        } else {
            badgeElement.style.display = 'none';
        }

        // بناء القائمة
        if (notifications.length === 0) {
            notificationList.innerHTML = '<div class="empty-msg">لا توجد إشعارات جديدة</div>';
            return;
        }

        let htmlContent = '';
        notifications.forEach(notif => {
            const date = new Date(notif.created_at).toLocaleDateString('ar-YE');
            const unreadClass = notif.is_read ? '' : 'unread';
            
            htmlContent += `
                <div class="notif-item ${unreadClass}">
                    <span class="notif-title">${notif.title}</span>
                    <span class="notif-msg">${notif.message}</span>
                    <span class="notif-date">📅 ${date}</span>
                </div>
            `;
        });
        notificationList.innerHTML = htmlContent;
    }

    // دالة فتح/إغلاق القائمة + تصفير العداد
    if (notificationBtn) {
        notificationBtn.addEventListener('click', async function(e) {
            e.stopPropagation(); // منع انتقال النقرة للنافذة
            
            // التبديل بين الإظهار والإخفاء
            const isVisible = notificationList.style.display === 'block';
            
            // إخفاء أي قوائم منسدلة أخرى أولاً
            document.querySelectorAll('.dropdown-menu').forEach(m => m.style.display = 'none');

            if (isVisible) {
                notificationList.style.display = 'none';
            } else {
                notificationList.style.display = 'block';

                // إذا كان هناك إشعارات غير مقروءة، قم بتعليمها كمقروءة الآن
                if (badgeElement.style.display !== 'none') {
                    // 1. إخفاء العداد بصرياً فوراً
                    badgeElement.style.display = 'none';
                    
                    // 2. إزالة التمييز (اللون الأزرق) من العناصر
                    const unreadItems = document.querySelectorAll('.notif-item.unread');
                    unreadItems.forEach(item => item.classList.remove('unread'));

                    // 3. إرسال الطلب للسيرفر في الخلفية
                    try {
                        await fetch('/api/notifications/mark-all-read/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        });
                    } catch (error) {
                        console.error('Failed to mark read:', error);
                    }
                }
            }
        });
    }

    // إغلاق قائمة الإشعارات عند النقر خارجها
    document.addEventListener('click', function(e) {
        if (notificationList && notificationList.style.display === 'block') {
            if (!notificationList.contains(e.target) && !notificationBtn.contains(e.target)) {
                notificationList.style.display = 'none';
            }
        }
    });

    // تشغيل جلب الإشعارات مرة واحدة عند التحميل
    fetchNotifications();

    // ============================================================
    // ⚙️ 2. صفحة إعداد خروج المغلوب (Knockout Setup)
    // ============================================================
    const teamCheckboxes = document.querySelectorAll('.team-check');
    const countBadge = document.getElementById('count-badge');
    const setupSubmitBtn = document.querySelector('button[type="submit"]');

    if (teamCheckboxes.length > 0 && countBadge) {
        
        function updateSelectedCount() {
            const count = document.querySelectorAll('.team-check:checked').length;
            countBadge.textContent = count;

            // التحقق من العدد المسموح (4, 8, 16, 32)
            const allowedCounts = [4, 8, 16, 32];
            
            if (allowedCounts.includes(count)) {
                countBadge.classList.remove('bg-danger');
                countBadge.classList.add('bg-success'); // أخضر
                if(setupSubmitBtn) setupSubmitBtn.disabled = false;
            } else {
                countBadge.classList.remove('bg-success');
                countBadge.classList.add('bg-danger'); // أحمر
                // if(setupSubmitBtn) setupSubmitBtn.disabled = true; // اختياري: تعطيل الزر
            }
        }

        // إضافة مستمع للأحداث لكل مربع اختيار
        teamCheckboxes.forEach(cb => {
            cb.addEventListener('change', updateSelectedCount);
        });

        // تشغيل الدالة عند التحميل لأول مرة
        updateSelectedCount();
    }

    // ============================================================
    // 📸 3. حفظ شجرة البطولة كصورة (Knockout Bracket)
    // ============================================================
    // ملاحظة: يجب إضافة زر له id="download-bracket-btn" في صفحة الشجرة
    const downloadBracketBtn = document.getElementById('download-bracket-btn');
    const bracketContainer = document.querySelector('.bracket-container');

    if (downloadBracketBtn && bracketContainer) {
        downloadBracketBtn.addEventListener('click', function() {
            const originalText = this.textContent;
            this.textContent = '...جاري المعالجة';

            if (typeof html2canvas !== 'undefined') {
                html2canvas(bracketContainer, {
                    backgroundColor: "#131201", // لون خلفية الصورة (نفس الثيم)
                    scale: 2, // جودة عالية
                    useCORS: true,
                    // إعدادات مهمة لتصوير العناصر التي بها Scroll أفقي
                    scrollX: 0,
                    scrollY: 0,
                    windowWidth: bracketContainer.scrollWidth,
                    width: bracketContainer.scrollWidth
                }).then(canvas => {
                    const leagueTitle = document.querySelector('h2')?.textContent.trim() || 'Tournament';
                    
                    const link = document.createElement('a');
                    link.download = `bracket-${leagueTitle}.png`;
                    link.href = canvas.toDataURL('image/png');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    this.textContent = originalText;
                }).catch(err => {
                    console.error('Bracket capture error:', err);
                    this.textContent = '❌ حدث خطأ';
                    setTimeout(() => { this.textContent = originalText; }, 3000);
                });
            } else {
                alert('مكتبة html2canvas غير متوفرة!');
                this.textContent = originalText;
            }
        });
    }

    // ... (بقية أكوادك السابقة هنا: التأثيرات، حفظ الجداول، إلخ) ...
    });
});