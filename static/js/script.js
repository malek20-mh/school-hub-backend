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
});