Sub InsertPhotos()
    
    'delete all photos for a fresh start!
    For Each pic In Worksheets("Senate").Pictures
        pic.Delete
    Next pic
    
    'loop through rows, excluding header to add matching photo
    For Counter = 2 To 43 'adjust to # rows in sheet
        
        Set curCell = Worksheets("Senate").Cells(Counter, 2) 'change all House to Senate when appropriate!
        curCell.Select
        
        Dim fileName As Variant
        fileName = Dir("/Users/tim/Dropbox/1_Work/ACLU/aclu-nm-legislator-scrape/legislator-photos/Senate")
        
        While fileName <> ""
        
            fullPath = "/Users/tim/Dropbox/1_Work/ACLU/aclu-nm-legislator-scrape/legislator-photos/Senate/" & fileName
            
            If Worksheets("Senate").Cells(Counter, 5) = CInt(Left(fileName, 2)) Then 'if the district matches, insert the photo
                                
                With Worksheets("Senate").Pictures.Insert( _
                    fullPath _
                     )
                   .ShapeRange.LockAspectRatio = msoTrue
                   .Height = 80
                   .Select
                End With
        
            End If

            fileName = Dir
    
        Wend
 
 Next Counter
 
 Rows("2:71").Select 'change index here to select all rows!
 Selection.RowHeight = 80
 
 Columns("B:B").Select
 Selection.ColumnWidth = 9
 
 End Sub
