from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_login import current_user
from wtforms.fields import FileField
import os
from shutil import rmtree
from werkzeug.utils import secure_filename
from models import Client
from flask_admin import BaseView,expose

document_root = 'documents'

class ExcelView(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/excel_view.html')



class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.name == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class ClientView(ModelView):

    form_extra_fields = {
        'pan': FileField('PAN Card'),
        'aadhar': FileField('AADHAR Card'),
        'passbook': FileField('Passbook')
    }

    form_excluded_columns = ('is_Eligible','pan_card','aadhar_card','bank_passbook')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.name == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))
    
    def on_model_change(self, form, model, is_created):

        if request.method == "POST":
            id = model.client_Id
            
            p = os.path.join(document_root,str(id))

            if not is_created:
                rmtree(p)
                model.pan_card = False
                model.aadhar_card = False
                model.bank_passbook =  False
            
            os.mkdir(p)

         

            for k in ['pan','aadhar','passbook']:

                if request.files[k]:
                    f = request.files[k]
                  
                    f.save(os.path.join(p,secure_filename(f.filename)))

                    if k == 'pan':
                        model.pan_card = True
                    elif k == 'aadhar':
                        model.aadhar_card = True
                    else:
                        model.bank_passbook = True

            
            if is_created:

                if model.agent_Id:
                    c = Client.query.filter_by(agent_Id=model.agent_Id).all()
                    
                    if len (c) >= 10:
                        a = Client.query.filter_by(client_Id=model.agent_Id).first()
                        a.is_Eligible = True
                        a.client_Share = 100
                        a.fund_Tree_Share = 0
                        
                    


                    
                


                
            
            

            
