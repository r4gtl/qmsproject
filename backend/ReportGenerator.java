import net.sf.jasperreports.engine.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;

public class ReportGenerator {
    public static void main(String[] args) {
        try {
            if (args.length < 6) {
                System.err.println(
                        "Usage: java ReportGenerator <template_path> <output_path> <db_url> <db_user> <db_password> [param1=value1 param2=value2 ...]");
                System.exit(1);
            }

            String templatePath = args[0];
            String outputPath = args[1];
            String dbUrl = args[2];
            String dbUser = args[3];
            String dbPassword = args[4];

            System.out.println("Template path: " + templatePath);
            System.out.println("Output path: " + outputPath);
            System.out.println("Database URL: " + dbUrl);

            Map<String, Object> parameters = new HashMap<>();
            for (int i = 5; i < args.length; i++) {
                String[] param = args[i].split("=", 2);
                if (param.length == 2) {
                    if (param[0].equals("PK")) {
                        try {
                            long pkValue = Long.parseLong(param[1]);
                            parameters.put(param[0], pkValue);
                            System.out.println("Parameter: " + param[0] + " = " + pkValue + " (Long)");
                        } catch (NumberFormatException e) {
                            System.err.println("Error: PK parameter must be a number");
                            System.exit(1);
                        }
                    } else {
                        parameters.put(param[0], param[1]);
                        System.out.println("Parameter: " + param[0] + " = " + param[1]);
                    }
                }
            }

            Class.forName("org.postgresql.Driver");
            System.out.println("PostgreSQL JDBC driver loaded.");

            Connection connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
            System.out.println("Database connection established.");

            
            

            System.out.println("Filling report with parameters: " + parameters);
            JasperPrint jasperPrint = JasperFillManager.fillReport(templatePath, parameters, connection);

            System.out.println("Report compiled successfully.");
            System.out.println("Number of pages: " + jasperPrint.getPages().size());

            JasperExportManager.exportReportToPdfFile(jasperPrint, outputPath);
            System.out.println("Report generated successfully: " + outputPath);

            connection.close();
            System.exit(0);
        } catch (Exception e) {
            System.err.println("Error generating report: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
