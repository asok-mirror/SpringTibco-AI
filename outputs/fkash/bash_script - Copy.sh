#!/bin/bash

# Set project name and directory
PROJECT_NAME="credit-maintenance"
BASE_DIR="$HOME/projects"
PROJECT_DIR="$BASE_DIR/$PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR/src/main/resources"
mkdir -p "$PROJECT_DIR/src/test/java/com/example/$PROJECT_NAME"

# Create pom.xml
cat << 'EOF' > "$PROJECT_DIR/pom.xml"
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.example</groupId>
	<artifactId>${PROJECT_NAME}</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>${PROJECT_NAME}</name>
	<description>${PROJECT_NAME} project</description>
	<properties>
		<java.version>21</java.version>
		<spring-boot.version>3.1.3</spring-boot.version>
	</properties>
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-jpa</artifactId>
			<version>${spring-boot.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-jms</artifactId>
			<version>${spring-boot.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
			<version>${spring-boot.version}</version>
		</dependency>

		<dependency>
			<groupId>com.oracle.database.jdbc</groupId>
			<artifactId>ojdbc8</artifactId>
			<version>21.1.0.1</version> <!-- Replace with your Oracle JDBC driver version -->
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
			<version>1.18.30</version>
			<optional>true</optional>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<version>${spring-boot.version}</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-csv</artifactId>
			<version>1.9.0</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/org.springframework.integration/spring-integration-core -->
		<dependency>
		    <groupId>org.springframework.integration</groupId>
		    <artifactId>spring-integration-core</artifactId>
		    <version>6.1.2</version>
		</dependency>
		
	</dependencies>
	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
				<version>${spring-boot.version}</version>
				<configuration>
					<excludes>
						<exclude>
							<groupId>org.projectlombok</groupId>
							<artifactId>lombok</artifactId>
						</exclude>
					</excludes>
				</configuration>
			</plugin>
		</plugins>
	</build>
</project>
EOF

# Create application.properties
cat << 'EOF' > "$PROJECT_DIR/src/main/resources/application.properties"
spring.application.name=${PROJECT_NAME}

# JMS Configuration
spring.jms.listener.auto-startup=true
spring.activemq.broker-url=tcp://localhost:61616
spring.activemq.user=admin
spring.activemq.password=admin

# Database Configuration
spring.datasource.url=jdbc:oracle:thin:@localhost:1521:xe # Replace with your database URL
spring.datasource.username=your_username # Replace with your database username
spring.datasource.password=your_password # Replace with your database password
spring.datasource.driver-class-name=oracle.jdbc.driver.OracleDriver
spring.jpa.hibernate.ddl-auto=none
EOF

# Create CreditMaintenanceApplication.java
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditMaintenanceApplication.java"
package com.example.${PROJECT_NAME};

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jms.annotation.EnableJms;

@SpringBootApplication
@EnableJms
@Slf4j
public class CreditMaintenanceApplication {

	public static void main(String[] args) {
		SpringApplication.run(CreditMaintenanceApplication.class, args);
		log.info("Credit Maintenance Application Started");
	}

}
EOF

# Create CreditMaintenanceListener.java
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditMaintenanceListener.java"
package com.example.${PROJECT_NAME};

import lombok.extern.slf4j.Slf4j;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class CreditMaintenanceListener {

    @JmsListener(destination = "M.MKT.CC2.CUSTOMER.MTNC.ACCOUNT.MAINTRIGGER")
    public void receiveMessage(String message) {
        log.info("Received message from M.MKT.CC2.CUSTOMER.MTNC.ACCOUNT.MAINTRIGGER: {}", message);
        // TODO: Implement the logic to process the message
    }

}
EOF

# Create CreditMaintenanceService.java
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditMaintenanceService.java"
package com.example.${PROJECT_NAME};

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class CreditMaintenanceService {

    public void processCreditMaintenance(String message) {
        log.info("Processing credit maintenance data: {}", message);
        // TODO: Implement the core business logic here
    }

}
EOF

# Create CreditMaintenanceController.java
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditMaintenanceController.java"
package com.example.${PROJECT_NAME};

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class CreditMaintenanceController {

    @Autowired
    private CreditMaintenanceService creditMaintenanceService;

    @GetMapping("/process")
    public String processCredit(@RequestParam String data) {
        log.info("Received request to process credit data: {}", data);
        creditMaintenanceService.processCreditMaintenance(data);
        return "Credit processing initiated";
    }

}
EOF

# Create CreditAccount.java (Entity)
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditAccount.java"
package com.example.${PROJECT_NAME};

import lombok.Data;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "CC_ODS_ACCOUNT_ADDITIONAL_ATTR")
@Data
public class CreditAccount {

    @Id
    private String accountNbr;
    private String accountTypeCd;
    // other fields

}
EOF

# Create CreditAccountRepository.java (Repository)
cat << 'EOF' > "$PROJECT_DIR/src/main/java/com/example/$PROJECT_NAME/CreditAccountRepository.java"
package com.example.${PROJECT_NAME};

import org.springframework.data.jpa.repository.JpaRepository;

public interface CreditAccountRepository extends JpaRepository<CreditAccount, String> {

}
EOF

# Create CreditMaintenanceServiceTest.java (Unit Test)
cat << 'EOF' > "$PROJECT_DIR/src/test/java/com/example/$PROJECT_NAME/CreditMaintenanceServiceTest.java"
package com.example.${PROJECT_NAME};

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class CreditMaintenanceServiceTest {

    @Autowired
    private CreditMaintenanceService creditMaintenanceService;

    @Test
    public void testProcessCreditMaintenance() {
        // TODO: Implement a proper unit test here
        creditMaintenanceService.processCreditMaintenance("test data");
        assertTrue(true); // Replace with actual assertion
    }
}
EOF

# Compile and run the project
cd "$PROJECT_DIR"
mvn clean install
mvn spring-boot:run
