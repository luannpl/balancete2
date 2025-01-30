from PySide6 import QtWidgets, QtGui, QtCore
from utils.icone import usar_icone
from db.conexao import conectar_com_banco
import sys

class UserLogin(QtWidgets.QWidget):
    def __init__(self):
        super(UserLogin, self).__init__()
        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet('background-color: #030d18;')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.user_label = QtWidgets.QLabel('Usuário:')
        self.user_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000; margin: 0px; padding: 0px;")
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setPlaceholderText('Digite o usuário')
        self.user_input.setStyleSheet("font-size: 20px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; color: #000000;") 

        self.password_label = QtWidgets.QLabel('Senha:')
        self.password_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000; margin: 0px; padding: 0px;")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText('Digite a senha')
        self.password_input.setStyleSheet("font-size: 20px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; color: #000000;")

        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.setStyleSheet("""QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            background-color: #001F3F;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #005588;  /* Cor de fundo quando o mouse passa sobre o botão */
            color:#ffffff;  /* Cor do texto quando o mouse passa sobre o botão */
        }""")
        self.login_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.clicked.connect(self.validate_login)

        self.cadastrar_button = QtWidgets.QPushButton('Cadastrar')
        self.cadastrar_button.setStyleSheet("""QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            background-color: #001F3F;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #005588;  /* Cor de fundo quando o mouse passa sobre o botão */
            color:#ffffff;  /* Cor do texto quando o mouse passa sobre o botão */
        }""")
        self.cadastrar_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cadastrar_button.clicked.connect(self.cadastrar_user)

        group_box = QtWidgets.QGroupBox()
        group_box.setStyleSheet("background-color: #FFFFFF; padding: 20px; border-radius: 10px;")
        group_box.setMaximumWidth(500) 
        group_box.setMinimumWidth(500)  

        group_box_layout = QtWidgets.QVBoxLayout()
        group_box_layout.setSpacing(10)  
        group_box_layout.setContentsMargins(10, 10, 10, 10) 
        group_box_layout.addWidget(self.user_label)
        group_box_layout.addWidget(self.user_input)
        group_box_layout.addWidget(self.password_label)
        group_box_layout.addWidget(self.password_input)
        group_box_layout.addWidget(self.login_button)
        group_box_layout.addWidget(self.cadastrar_button)
        group_box.setLayout(group_box_layout)

        center_layout = QtWidgets.QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(group_box, alignment=QtCore.Qt.AlignCenter)
        center_layout.addStretch()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(center_layout)

        self.setLayout(main_layout)
    
    def validate_login(self):
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("USE railway")
        cursor.execute("SELECT senha FROM user WHERE nome = %s", (user,))
        result = cursor.fetchone()
        
        if not result:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle('Erro')
            msg_box.setText('Usuário ou senha inválidos.')
            usar_icone(msg_box)
            msg_box.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 20px; font-weight: bold;")
            msg_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    
            msg_box.exec()
            return
        result = result[0]
        

        if password == result:
            self.empresa_window = EmpresaWindow(user)
            usar_icone(self.empresa_window)
            self.empresa_window.showMaximized()
            self.close()
        else:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle('Erro')
            msg_box.setText('Usuário ou senha inválidos.')
            usar_icone(msg_box)
            msg_box.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 20px; font-weight: bold;")
            msg_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    
            msg_box.exec()
            return
    
    def cadastrar_user(self):
        self.cadastro = UserCadastro()
        usar_icone(self.cadastro)
        self.cadastro.showMaximized()
        self.close()

class UserCadastro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro')
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet('background-color: #030d18;')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.user_label = QtWidgets.QLabel('Usuário:')
        self.user_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000; margin: 0px; padding: 0px;")
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setPlaceholderText('Digite o usuário')
        self.user_input.setStyleSheet("font-size: 20px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; color: #000000;") 

        # Campo de entrada para senha
        self.password_label = QtWidgets.QLabel('Senha:')
        self.password_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000; margin: 0px; padding: 0px;")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText('Digite a senha')
        self.password_input.setStyleSheet("font-size: 20px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; color: #000000;")


        # Botão para login
        self.cadastrar_button = QtWidgets.QPushButton('Cadastrar')
        self.cadastrar_button.setStyleSheet("""QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            background-color: #001F3F;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #005588;  /* Cor de fundo quando o mouse passa sobre o botão */
            color:#ffffff;  /* Cor do texto quando o mouse passa sobre o botão */
        }""")
        self.cadastrar_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cadastrar_button.clicked.connect(self.cadastrar_user)

        self.voltar_btn = QtWidgets.QPushButton('Voltar')
        self.voltar_btn.setStyleSheet("""QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            background-color: #001F3F;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #005588;  /* Cor de fundo quando o mouse passa sobre o botão */
            color:#ffffff;  /* Cor do texto quando o mouse passa sobre o botão */
        }""")
        self.voltar_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.voltar_btn.clicked.connect(self.voltar)

        group_box = QtWidgets.QGroupBox()
        group_box.setStyleSheet("background-color: #FFFFFF; padding: 20px; border-radius: 10px;")
        group_box.setMaximumWidth(500)  # Aumentando a largura máxima do grupo
        group_box.setMinimumWidth(500)  # Define uma largura mínima para evitar colapso

        # Adiciona o layout ao grupo
        group_box_layout = QtWidgets.QVBoxLayout()
        group_box_layout.setSpacing(10)  # Ajusta o espaçamento vertical entre os widgets
        group_box_layout.setContentsMargins(10, 10, 10, 10)  # Ajusta margens internas do grupo
        group_box_layout.addWidget(self.user_label)
        group_box_layout.addWidget(self.user_input)
        group_box_layout.addWidget(self.password_label)
        group_box_layout.addWidget(self.password_input)
        group_box_layout.addWidget(self.cadastrar_button)
        group_box_layout.addWidget(self.voltar_btn)
        group_box.setLayout(group_box_layout)

        center_layout = QtWidgets.QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(group_box, alignment=QtCore.Qt.AlignCenter)
        center_layout.addStretch()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(center_layout)

        self.setLayout(main_layout)    

    def cadastrar_user(self):
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()
        print(user, password)
        print(len(user), len(password))
        if len(user) < 1:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle('Erro')
            msg_box.setText('Usuário precisa ter pelo menos um caractere.')
            usar_icone(msg_box)
            msg_box.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 16px; font-weight: bold;")
            msg_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    
            msg_box.exec()
            return
        if len(password) < 1:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle('Erro')
            msg_box.setText('Senha precisa ter pelo menos um caractere.')
            usar_icone(msg_box)
            msg_box.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 16px; font-weight: bold;")
            msg_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    
            msg_box.exec()
            return

        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("USE railway")
        cursor.execute("INSERT INTO user (nome, senha) VALUES (%s, %s)", (user, password))
        conexao.commit()
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setWindowTitle('Sucesso')
        msg_box.setText('Usuário cadastrado com sucesso.')
        usar_icone(msg_box)
        msg_box.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 16px; font-weight: bold;")
        msg_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    
        msg_box.exec()
        self.close()    

    def voltar(self):
        self.login = UserLogin()
        usar_icone(self.login)
        self.login.showMaximized()
        self.close()    

class EmpresaWindow(QtWidgets.QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Empresas')
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet('background-color: #030d18;')

        self.user = user
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.label_titulo = QtWidgets.QLabel('Escolha ou cadastre uma empresa')
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; margin: 0px; padding: 0px;")
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        
        self.layout.addWidget(self.label_titulo)

        self.layout.addSpacing(20)

        self.combo_empresas = QtWidgets.QComboBox()
        self.combo_empresas.setStyleSheet("font-size: 20px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; color:rgb(255, 255, 255);")
        self.combo_empresas.setFixedWidth(400)
        self.carregar_empresas()
    
        self.layout.addWidget(self.combo_empresas, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def carregar_empresas(self):
        conexao = conectar_com_banco()
        try:
            cursor = conexao.cursor()
            cursor.execute("USE railway")
            cursor.execute("SELECT nome FROM empresas ORDER BY nome ASC")
            empresas = [row[0] for row in cursor.fetchall()]
            
            self.combo_empresas.clear()
            self.combo_empresas.addItems(empresas)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao acessar o banco de dados: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
        
class MainWindow(QtWidgets.QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Consultor de Produto')
        self.setGeometry(400, 200, 900, 700)
        self.setStyleSheet("background-color: #030d18;")

def main():
    app = QtWidgets.QApplication(sys.argv)
    login = UserLogin()
    usar_icone(login)
    login.showMaximized()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()