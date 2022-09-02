

Sub Macro1()
'
' Macro1 Macro
'
'

    Dim LastRow As Long
    Dim fileName As Variant
    fileName = Dir("/Users/tim/Dropbox/1_Work/ACLU/aclu-nm-legislator-scrape/votes-csvs/19-Special/")
    
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "Header Cell" '
    'GrantAccessToMultipleFiles (Array(fileName))
    
    While fileName <> ""
    
            'Debug.Print (fileName)
            fullPath = "/Users/tim/Dropbox/1_Work/ACLU/aclu-nm-legislator-scrape/votes-csvs/19-Special/" & fileName
            connString = "TEXT;" & fullPath
            Debug.Print (connString)
            NextRow = ActiveSheet.Cells.Find("*", SearchOrder:=xlByRows, SearchDirection:=xlPrevious).Row + 2
            Debug.Print (NextRow)
            
            Application.CutCopyMode = False
            With ActiveSheet.QueryTables.Add(Connection:= _
                connString _
                , Destination:=Range("$A$2"))
                .Name = "_22_Regular_HB0001HVOTE_3"
                .FieldNames = True
                .RowNumbers = False
                .FillAdjacentFormulas = False
                .PreserveFormatting = True
                .RefreshOnFileOpen = False
                .RefreshStyle = xlInsertDeleteCells
                .SavePassword = False
                .SaveData = True
                .RefreshPeriod = False
                .TextFilePromptOnRefresh = False
                .TextFilePlatform = 65001
                .TextFileStartRow = 1
                .TextFileParseType = xlDelimited
                .TextFileTextQualifier = xlTextQualifierDoubleQuote
                .TextFileConsecutiveDelimiter = False
                .TextFileTabDelimiter = False
                .TextFileSemicolonDelimiter = False
                .TextFileCommaDelimiter = True
                .TextFileSpaceDelimiter = False
                .TextFileColumnDataTypes = Array(1, 1, 1, 1, 1, 1)
                .TextFileTrailingMinusNumbers = True
                .Refresh BackgroundQuery:=False
            End With
            
            fileName = Dir
            
        Wend

End Sub



