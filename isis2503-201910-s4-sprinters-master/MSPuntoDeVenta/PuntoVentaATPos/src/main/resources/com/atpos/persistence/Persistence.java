package com.atpos.persistence;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import com.atpos.vo.VOEmpleado;
import com.atpos.vo.VOPuntoVenta;

public class Persistence 
{
	
	private  Connection conn;
	
	public Persistence() {
		
		
		conectarse();
	}
	
	public void createPuntoVenta(String direccion, String negocio)
	{
		try 
		{
			Statement st = conn.createStatement();
			String sql = "INSERT INTO puntoventa (direccion,negocio) VALUES ('"+direccion+"','"+negocio+"')";
			st.execute(sql);
			conn.close();
			
		} 
		catch (SQLException e) 
		{
			e.printStackTrace();
		}
	}
	
	
	public void createEmpleado(String nombre , String cedula, String apellido, String rol, String email, int salario)
	{
		try 
		{
			Statement st = conn.createStatement();
			String sql = "INSERT INTO empleado (nombre,cedula,apellido,rol,email,salario) VALUES ('"+nombre+"','"+cedula+"','"+apellido+"','"+rol+"','"+email+"',"+salario+")";
			st.execute(sql);
			conn.close();

			
		} 
		catch (SQLException e) 
		{
			e.printStackTrace();
		}
	}
	
	public ArrayList<VOPuntoVenta> obtenerPuntosVenta()
	{
		try 
		{
			ArrayList<VOPuntoVenta> listaTotal = new ArrayList<VOPuntoVenta>();
			Statement st = conn.createStatement();
			String sql = "SELECT * FROM puntoventa";
			ResultSet rs = st.executeQuery(sql);
			
			System.out.println(rs);
			
			while (rs.next()) 
			{
				String direccion = rs.getString("direccion");
				String negocio = rs.getString("negocio");
				
				listaTotal.add(new VOPuntoVenta(direccion, negocio));
			}
			conn.close();
			return listaTotal;
			
		} catch (SQLException e) 
		{
			e.printStackTrace();
			return null;
			
		}
	}
	
	public ArrayList<VOEmpleado> obtenerEmpleados()
	{
		try 
		{
			ArrayList<VOEmpleado> listaTotal = new ArrayList<VOEmpleado>();
			Statement st = conn.createStatement();
			String sql = "SELECT * FROM empleado";
			ResultSet rs = st.executeQuery(sql);
			
			while (rs.next()) 
			{
				String nombre = rs.getString("nombre");
				String apellido = rs.getString("apellido");
				String email = rs.getString("email");
				Integer salario = rs.getInt("salario");
				String rol = rs.getString("rol");
				String cedula = rs.getString("cedula");


				listaTotal.add(new VOEmpleado(nombre,apellido,cedula,salario,rol,email ));
			}
			conn.close();

			
			return listaTotal;
			
		} 
		catch (SQLException e) 
		{
			e.printStackTrace();
			return null;
			
		} catch (Exception e) 
		{
			e.printStackTrace();
			return null;
		}
	}
	
	public  void conectarse()
	{
		try
		{
			Class.forName("oracle.jdbc.OracleDriver");
			
			 conn =  DriverManager.getConnection("jdbc:oracle:thin:@fn3.oracle.virtual.uniandes.edu.co:1521:prod","ISIS2304M041910","bZqmnNScyi");
			
		}
		catch (Exception e) 
		{
		}
	}

}
