import secrets
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from registrations.models import Registration
from .models import Certificate
from audit.models import AuditLog

def _is_organizer(user):
    return getattr(getattr(user, 'profile', None), 'role', None) == 'organizador'

@login_required
def my_certificates(request):
    """List all certificates for the logged-in user"""
    certificates = Certificate.objects.filter(
        registration__user=request.user
    ).select_related('registration__event')
    
    return render(request, 'certificates/my_certificates.html', {
        'certificates': certificates
    })

@login_required
def issue(request, registration_id):
    if not _is_organizer(request.user):
        messages.error(request, 'Apenas organizadores podem emitir certificados.')
        return redirect('home')

    reg = get_object_or_404(Registration, id=registration_id)
    cert, created = Certificate.objects.get_or_create(
        registration=reg,
        defaults={'code': secrets.token_hex(8)}
    )
    if created:
        messages.success(request, 'Certificado emitido com sucesso.')
    return redirect('download_certificate', certificate_id=cert.id)

@login_required
def download(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    
    # Permission check: Only the owner or an organizer can download
    if certificate.registration.user != request.user and not _is_organizer(request.user):
        messages.error(request, 'Você não tem permissão para baixar este certificado.')
        return redirect('my_certificates')
    
    # Log certificate download
    AuditLog.objects.create(
        user=request.user,
        action='DOWNLOAD_CERTIFICATE',
        target_model='Certificate',
        target_id=certificate.id,
        details=f'Download de certificado: {certificate.registration.user.username} - {certificate.registration.event.title}'
    )
    
    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{certificate.code}.pdf"'
    
    pdf_canvas = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Header
    pdf_canvas.setFont("Helvetica-Bold", 20)
    pdf_canvas.drawCentredString(width / 2, height - 100, "CERTIFICADO DE PARTICIPAÇÃO")
    
    # Content
    pdf_canvas.setFont("Helvetica", 12)
    text_y = height - 150
    pdf_canvas.drawCentredString(width / 2, text_y, f"Certificamos que {certificate.registration.user.get_full_name() or certificate.registration.user.username}")
    pdf_canvas.drawCentredString(width / 2, text_y - 30, f"participou do evento: {certificate.registration.event.title}")
    pdf_canvas.drawCentredString(width / 2, text_y - 60, f"realizado de {certificate.registration.event.start_date} a {certificate.registration.event.end_date}")
    
    # Footer
    pdf_canvas.setFont("Helvetica-Oblique", 10)
    pdf_canvas.drawCentredString(width / 2, 100, f"Código de Verificação: {certificate.code}")
    pdf_canvas.drawCentredString(width / 2, 80, f"Emitido em: {certificate.issued_at.strftime('%d/%m/%Y')}")
    
    pdf_canvas.showPage()
    pdf_canvas.save()
    return response
