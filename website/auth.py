from .models import Company
from . import db

@auth.route('/companyReg', methods=['GET', 'POST'])
def companyReg():
    if request.method == 'POST':
        company_name = request.form.get('companyName')
        company_owner = request.form.get('companyOwner')
        mailing_address = request.form.get('mailingAddress')
        official_email = request.form.get('officialEmail')
        official_phone_number = request.form.get('officialPhoneNumber')
        industry_type = request.form.get('industryType')

        company = Company.query.filter_by(email=official_email).first()
        if company:
            flash('Company with this email already exists.', category='error')
        elif len(official_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(company_name) < 2:
            flash('Company name must be greater than 1 character.', category='error')
        elif len(company_owner) < 2:
            flash('Company owner name must be greater than 1 character.', category='error')
        elif len(official_phone_number) < 10:
            flash('Phone number must be at least 7 characters.', category='error')
        else:
            new_company = Company(
                name=company_name,
                owner=company_owner,
                mailing_address=mailing_address,
                email=official_email,
                phone_number=official_phone_number,
                industry=industry_type
            )
            db.session.add(new_company)
            db.session.commit()
            flash('Company registered successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("companyReg.html", user=current_user)

