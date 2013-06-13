VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   5940
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   6675
   LinkTopic       =   "Form1"
   ScaleHeight     =   5940
   ScaleWidth      =   6675
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame1 
      Caption         =   "ÉtÉåÅ[ÉÄÇP"
      BeginProperty Font 
         Name            =   "ÇlÇr ÉSÉVÉbÉN"
         Size            =   9
         Charset         =   128
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   3615
      Left            =   3480
      TabIndex        =   2
      Top             =   1680
      Width           =   3015
      Begin VB.Label Label1 
         Caption         =   "ÉâÉxÉãÇR"
         BeginProperty Font 
            Name            =   "ÇlÇr ÉSÉVÉbÉN"
            Size            =   9
            Charset         =   128
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   615
         Index           =   1
         Left            =   840
         TabIndex        =   3
         Top             =   840
         Width           =   1095
      End
   End
   Begin VB.Label Label2 
      Caption         =   "ÉâÉxÉãÇQ"
      BeginProperty Font 
         Name            =   "ÇlÇr ñæí©"
         Size            =   9
         Charset         =   128
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   735
      Left            =   840
      TabIndex        =   1
      Top             =   2160
      Width           =   1335
   End
   Begin VB.Label Label1 
      Caption         =   "ÉâÉxÉãÇP"
      BeginProperty Font 
         Name            =   "ÇlÇr ÇoÉSÉVÉbÉN"
         Size            =   9.75
         Charset         =   128
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   615
      Index           =   0
      Left            =   840
      TabIndex        =   0
      Top             =   600
      Width           =   1815
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Form_Load()
    Label1(1).Caption = LoadResString(1004)
    Frame1.Caption = LoadResString(1005)
    Label2.Caption = LoadResString(1006)
    Label1(0).Caption = LoadResString(1007)

Label2.Caption = LoadResString(1001)
    
End Sub

Private Sub Label1_Click(Index As Integer)
    Form1.Caption = LoadResString(1002)
    
    Label1(1).Caption = GetName()
    
End Sub

Private Sub Label2_Click()
    Dim p As People
    Set p = New People
    p.m_Name = LoadResString(1003)
        
    
    Label1(0).Caption = p.m_Name
End Sub
