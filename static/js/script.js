document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================================
    // 🔔 1. نظام الإشعارات (Notifications System)
    // ============================================================
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationList = document.getElementById('notificationList');
    const badgeElement = document.getElementById('notificationBadge');

    // دالة مساعدة لجلب CSRF Token
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
        if (!notificationBtn) return; // المستخدم غير مسجل دخول
        
        try {
            const response = await fetch('/api/notifications/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include' // ✅ أهم سطر للمصادقة
            });

            if (response.ok) {
                const data = await response.json();
                updateNotificationUI(data);
            } else {
                console.error('Server returned:', response.status);
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }

    // دالة تحديث واجهة الإشعارات
    function updateNotificationUI(notifications) {
        if (!notificationList || !badgeElement) return;

        const unreadCount = notifications.filter(n => !n.is_read).length;

        // تحديث العداد الأحمر
        if (unreadCount > 0) {
            badgeElement.textContent = unreadCount;
            badgeElement.style.display = 'block';
            badgeElement.style.animation = 'bounce 0.5s ease';
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

    // التعامل مع النقر على زر الجرس
    if (notificationBtn) {
        notificationBtn.addEventListener('click', async function(e) {
            e.stopPropagation();
            
            const isVisible = notificationList.style.display === 'block';
            
            // إخفاء القوائم الأخرى
            document.querySelectorAll('.dropdown-menu').forEach(m => m.style.display = 'none');

            if (isVisible) {
                notificationList.style.display = 'none';
            } else {
                notificationList.style.display = 'block';

                // تعليم الكل كمقروء إذا كان هناك جديد
                if (badgeElement.style.display !== 'none') {
                    badgeElement.style.display = 'none';
                    const unreadItems = document.querySelectorAll('.notif-item.unread');
                    unreadItems.forEach(item => item.classList.remove('unread'));

                    try {
                        await fetch('/api/notifications/mark-all-read/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            credentials: 'include' // ✅ مهم أيضاً للـ POST
                        });
                    } catch (error) {
                        console.error('Failed to mark read:', error);
                    }
                }
            }
        });
    }

    // إغلاق القائمة عند النقر في الخارج
    document.addEventListener('click', function(e) {
        if (notificationList && notificationList.style.display === 'block') {
            if (!notificationList.contains(e.target) && !notificationBtn.contains(e.target)) {
                notificationList.style.display = 'none';
            }
        }
    });

    // تشغيل الإشعارات (لأول مرة + تكرار دوري)
    fetchNotifications();
    setInterval(fetchNotifications, 10000); // كل 10 ثواني

    // ============================================================
    // ✨ 2. تأثيرات عامة (UI Effects)
    // ============================================================
    
    // تنظيف تأثيرات البطاقات
    const cards = document.querySelectorAll('.card-3d');
    cards.forEach(card => {
        card.removeEventListener('mousemove', function(){});
        card.removeEventListener('mouseleave', function(){});
    });

    // تأثيرات حقول الإدخال
    const formInputs = document.querySelectorAll('.modern-form input, .modern-form select, .modern-form textarea');
    formInputs.forEach(input => {
        if (!input.parentElement.classList.contains('icon-field-wrapper')) {
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

    // تأثيرات الجداول
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

    // ============================================================
    // 📸 3. وظائف التحميل كصورة (Image Export)
    // ============================================================

    // دالة عامة لاستخدام html2canvas لتجنب التكرار
    function captureAndDownload(elementId, btnElement, fileNamePrefix, scale=2) {
        const elementToSave = document.getElementById(elementId);
        if (!elementToSave) return;

        const originalText = btnElement.textContent;
        btnElement.textContent = '...جاري التحضير';

        if (typeof html2canvas !== 'undefined') {
            html2canvas(elementToSave, {
                backgroundColor: "#131201",
                scale: scale,
                useCORS: true,
                scrollX: 0,
                scrollY: 0,
                windowWidth: elementToSave.scrollWidth,
                width: elementToSave.scrollWidth
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = `${fileNamePrefix}-${new Date().getTime()}.png`;
                link.href = canvas.toDataURL('image/png');
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                btnElement.textContent = originalText;
            }).catch(err => {
                console.error('Capture error:', err);
                btnElement.textContent = '❌ فشل';
                setTimeout(() => { btnElement.textContent = originalText; }, 3000);
            });
        } else {
            alert('مكتبة التصوير غير محملة');
            btnElement.textContent = originalText;
        }
    }

    // 1. حفظ صورة المجموعة
    const saveButtons = document.querySelectorAll('.btn-save-group');
    saveButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const targetId = this.getAttribute('data-target-id');
            captureAndDownload(targetId, this, 'standings');
        });
    });

    // 2. حفظ قائمة الهدافين
    const downloadScorersBtn = document.getElementById('download-scorers-btn');
    if (downloadScorersBtn) {
        downloadScorersBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            captureAndDownload('scorers-card-to-save', this, 'scorers');
        });
    }

    // 3. حفظ بطاقة المباراة
    const downloadMatchBtn = document.getElementById('download-match-card-btn');
    if (downloadMatchBtn) {
        downloadMatchBtn.addEventListener('click', function() {
            captureAndDownload('match-card-to-save', this, 'match-card');
        });
    }

    // 4. حفظ جدول المباريات
    const downloadScheduleBtn = document.getElementById('download-schedule-btn');
    if (downloadScheduleBtn) {
        downloadScheduleBtn.addEventListener('click', function() {
            captureAndDownload('schedule-to-capture', this, 'schedule', 3);
        });
    }

    // 5. حفظ شجرة البطولة
    const downloadBracketBtn = document.getElementById('download-bracket-btn');
    if (downloadBracketBtn) {
        downloadBracketBtn.addEventListener('click', function() {
            // نمرر الكلاس كـ ID للدالة المساعدة (تعديل بسيط للدالة قد يلزم، لكن هنا سنستخدم المنطق المباشر)
            const bracketContainer = document.querySelector('.bracket-container');
            if (bracketContainer) {
                // نعطيها ID مؤقت إذا لم يكن لها
                if (!bracketContainer.id) bracketContainer.id = 'temp-bracket-id';
                captureAndDownload(bracketContainer.id, this, 'bracket');
            }
        });
    }

    // ============================================================
    // ⚙️ 4. إدارة القوائم المنسدلة والإعدادات
    // ============================================================
    
    // القوائم المنسدلة
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = this.nextElementSibling;
            if (menu) {
                document.querySelectorAll('.dropdown-menu').forEach(m => {
                    if (m !== menu) m.style.display = 'none';
                });
                menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
            }
        });
    });

    // إغلاق القوائم عند النقر خارجها
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.dropdown-toggle')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    // صفحة إعداد خروج المغلوب (Knockout Setup)
    const teamCheckboxes = document.querySelectorAll('.team-check');
    const countBadge = document.getElementById('count-badge');
    const setupSubmitBtn = document.querySelector('button[type="submit"]');

    if (teamCheckboxes.length > 0 && countBadge) {
        function updateSelectedCount() {
            const count = document.querySelectorAll('.team-check:checked').length;
            countBadge.textContent = count;
            const allowedCounts = [4, 8, 16, 32];
            
            if (allowedCounts.includes(count)) {
                countBadge.classList.remove('bg-danger');
                countBadge.classList.add('bg-success');
                if(setupSubmitBtn) setupSubmitBtn.disabled = false;
            } else {
                countBadge.classList.remove('bg-success');
                countBadge.classList.add('bg-danger');
                // if(setupSubmitBtn) setupSubmitBtn.disabled = true;
            }
        }
        teamCheckboxes.forEach(cb => {
            cb.addEventListener('change', updateSelectedCount);
        });
        updateSelectedCount();
    }

}); // نهاية DOMContentLoaded