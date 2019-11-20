package com.atpos.vo;

public class VOEmpleado {
	
	
	public static final String ADMIN="ADMIN";
	public static final String CAJERO="CAJERO";



	private String nombre;

	private String apellido;
	
	private String cedula;
	
	private int salario;

	private String rol;
	
	private String email;
	
	
	public VOEmpleado(String nombre, String apellido, String cedula, int salario, String rol, String email) throws Exception 
	{
		if(verificarRol(rol))
		{
			this.nombre = nombre;
			this.apellido = apellido;
			this.salario = salario;
			this.cedula = cedula;
			this.rol = rol;
			this.email = email;
		}
		else
		{
			throw new Exception("Rol no permitido");
		}

	}
	
	public VOEmpleado()
	{
		//
	}
	
	public String getCedula() {
		return cedula;
	}

	public void setCedula(String cedula) {
		this.cedula = cedula;
	}

	public String getRol() 
	{
		return rol;
	}

	public void setRol(String rol) 
	{
		this.rol = rol;
	}

	public String getNombre() 
	{
		return nombre;
	}

	public void setNombre(String nombre) 
	{
		this.nombre = nombre;
	}

	public String getApellido() 
	{
		return apellido;
	}

	public void setApellido(String apellido) 
	{
		this.apellido = apellido;
	}

	public int getSalario() 
	{
		return salario;
	}

	public void setSalario(int salario) 
	{
		this.salario = salario;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}
	
	public boolean verificarRol(String rol)
	{
		if(rol.equals(ADMIN) || rol.equals(CAJERO))
		{
			return true;
		}
		return false;
	}
	





}
