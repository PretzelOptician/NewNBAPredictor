import static org.apache.poi.ss.usermodel.Cell.CELL_TYPE_NUMERIC;

import java.io.FileInputStream;  
import java.io.FileNotFoundException;  
import java.io.IOException;  
import org.apache.poi.ss.usermodel.Cell;  
import org.apache.poi.ss.usermodel.*;  
import org.apache.poi.ss.usermodel.Sheet;  
import org.apache.poi.ss.usermodel.Workbook;  
import org.apache.poi.xssf.usermodel.XSSFWorkbook;  

public class ReadExcelFileDemo  {  
	 /*public static void main(String[] args) {
		ReadExcelFileDemo rc=new ReadExcelFileDemo();   //object of the class  
		//reading the value of 2nd row and 2nd column  
		String vOutput=rc.ReadCellData(1, 1);   
		System.out.println(vOutput);  
	}*/
	static String stringValue=null;          //variable for storing the cell value  
	static double doubleValue=0.0; 
	//method defined for reading a cell  
	public static void ReadCellData(int vRow, int vColumn, String teamName)  
	{  
	Workbook wb=null;           //initialize Workbook null  
	try  
	{  
	//reading data from a file in the form of bytes  
	FileInputStream fis=new FileInputStream("C:\\Users\\aweso\\OneDrive\\Desktop\\NBA-Spreadsheets\\" + teamName + "Stats.xlsx");  
	//constructs an XSSFWorkbook object, by buffering the whole stream into the memory  
	wb=new XSSFWorkbook(fis);  
	}  
	catch(FileNotFoundException e)  
	{  
	e.printStackTrace();  
	}  
	catch(IOException e1)  
	{  
	e1.printStackTrace();  
	}  
	Sheet sheet=wb.getSheetAt(0);   //getting the XSSFSheet object at given index  
	FormulaEvaluator formulaEvaluator=wb.getCreationHelper().createFormulaEvaluator(); 
	Row row=sheet.getRow(vRow); //returns the logical row  
	Cell cell=row.getCell(vColumn); //getting the cell representing the given column 
	switch(formulaEvaluator.evaluateInCell(cell).getCellType()) {
		case Cell.CELL_TYPE_STRING:
			stringValue=cell.getStringCellValue();    //getting cell value  
			break;
		case CELL_TYPE_NUMERIC: 
			doubleValue=cell.getNumericCellValue();
			break;
	}
	//return value;               //returns the cell value  
}  
	public static double returnDouble(int row, int column, String teamName) {
		ReadExcelFileDemo.ReadCellData(row, column, teamName);
		return doubleValue; 
	}
	public static String returnString(int row, int column, String teamName) {
		ReadExcelFileDemo.ReadCellData(row, column, teamName); 
		return stringValue; 
	}
}  