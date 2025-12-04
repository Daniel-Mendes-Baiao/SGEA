from io import StringIO, BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from events.models import Event
from registrations.models import Registration

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def _is_organizer(user):
    return getattr(getattr(user, 'profile', None), 'role', None) == 'organizador'

def _check_perm(user):
    if not _is_organizer(user):
        raise Http404  # manter simples/“estilo aluno”

@login_required
def event_registrations(request, event_id):
    _check_perm(request.user)
    event = get_object_or_404(Event, id=event_id)
    regs = Registration.objects.filter(event=event).select_related('user')
    return render(request, 'reports/event_regs.html', {'event': event, 'regs': regs})

@login_required
def event_registrations_csv(request, event_id):
    _check_perm(request.user)
    event = get_object_or_404(Event, id=event_id)
    regs = Registration.objects.filter(event=event).select_related('user')

    buf = StringIO()
    buf.write('username,nome,email,created_at\n')
    for r in regs:
        u = r.user
        nome = f'{u.first_name} {u.last_name}'.strip()
        buf.write(f'{u.username},{nome},{u.email},{r.created_at.isoformat()}\n')

    resp = HttpResponse(buf.getvalue(), content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = f'attachment; filename=inscritos_evento_{event.id}.csv'
    return resp

@login_required
def event_registrations_pdf(request, event_id):
    _check_perm(request.user)
    event = get_object_or_404(Event, id=event_id)
    regs = Registration.objects.filter(event=event).select_related('user')

    buf = BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    p.setFont('Helvetica-Bold', 14)
    p.drawString(50, H-60, f'Inscritos — {event.title}')
    p.setFont('Helvetica', 10)
    y = H-90
    p.drawString(50, y, 'username'); p.drawString(180, y, 'nome'); p.drawString(400, y, 'email'); p.drawString(520, y, 'inscrito_em')
    y -= 15

    for r in regs:
        u = r.user
        nome = f'{u.first_name} {u.last_name}'.strip()
        p.drawString(50, y, u.username[:20])
        p.drawString(180, y, nome[:30])
        p.drawString(400, y, (u.email or '')[:30])
        p.drawString(520, y, r.created_at.strftime('%d/%m/%Y'))
        y -= 15
        if y < 50:
            p.showPage()
            y = H-60

    p.showPage()
    p.save()
    pdf = buf.getvalue()
    buf.close()
    resp = HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename=inscritos_evento_{event.id}.pdf'
    return resp
