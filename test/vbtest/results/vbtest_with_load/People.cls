VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "People"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder6" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
'local variable(s) to hold property value(s)
Private mvarm_Name As String 'local copy
Public Property Let m_Name(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.m_Name = 5
    mvarm_Name = vData
End Property


Public Property Get m_Name() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.m_Name
    m_Name = LoadResString(1001) & mvarm_Name
End Property



