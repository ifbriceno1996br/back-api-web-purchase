-- Script para crear stored procedures en SQL Server
-- Este script debe ejecutarse en la base de datos del proyecto

-- 1. SP para obtener reporte de solicitudes
CREATE OR ALTER PROCEDURE sp_GetRequestReport
    @StartDate DATE = NULL,
    @EndDate DATE = NULL,
    @Status VARCHAR(20) = NULL,
    @UserId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        r.id AS RequestId,
        r.title AS RequestTitle,
        r.description AS RequestDescription,
        r.status AS RequestStatus,
        r.amount AS RequestAmount,
        r.expected_date AS ExpectedDate,
        r.created_at AS RequestCreatedAt,
        r.updated_at AS RequestUpdatedAt,
        
        -- Información del usuario que creó la solicitud
        u.email AS RequestCreatorEmail,
        u.full_name AS RequestCreatorName,
        
        -- Información del supervisor
        s.email AS SupervisorEmail,
        s.full_name AS SupervisorName,
        
        -- Último cambio de estado
        (
            SELECT TOP 1 ar.new_status 
            FROM audit_requests ar 
            WHERE ar.request_id = r.id 
            AND ar.action = 'status_change'
            ORDER BY ar.created_at DESC
        ) AS LastStatusChange,
        
        -- Fecha del último cambio de estado
        (
            SELECT TOP 1 ar.created_at 
            FROM audit_requests ar 
            WHERE ar.request_id = r.id 
            AND ar.action = 'status_change'
            ORDER BY ar.created_at DESC
        ) AS LastStatusChangeDate,
        
        -- Comentario del último cambio de estado
        (
            SELECT TOP 1 ar.comment 
            FROM audit_requests ar 
            WHERE ar.request_id = r.id 
            AND ar.action = 'status_change'
            ORDER BY ar.created_at DESC
        ) AS LastStatusComment,
        
        -- Cantidad de comentarios
        (
            SELECT COUNT(*) 
            FROM comment_requests cr 
            WHERE cr.request_id = r.id
        ) AS CommentCount,
        
        -- Tiempo en días desde la creación
        DATEDIFF(day, r.created_at, GETDATE()) AS DaysSinceCreation,
        
        -- Tiempo en días hasta la fecha esperada
        DATEDIFF(day, GETDATE(), r.expected_date) AS DaysUntilExpectedDate
    FROM 
        requests r
        INNER JOIN users u ON r.user_id = u.id
        LEFT JOIN users s ON r.supervisor_id = s.id
    WHERE 
        (@StartDate IS NULL OR r.created_at >= @StartDate)
        AND (@EndDate IS NULL OR r.created_at <= @EndDate)
        AND (@Status IS NULL OR r.status = @Status)
        AND (@UserId IS NULL OR r.user_id = @UserId)
    ORDER BY 
        r.created_at DESC;
END
GO

-- 2. SP para obtener estadísticas de solicitudes por usuario
CREATE OR ALTER PROCEDURE sp_GetUserRequestStats
    @UserId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        u.id AS UserId,
        u.email AS UserEmail,
        u.full_name AS UserName,
        COUNT(r.id) AS TotalRequests,
        SUM(CASE WHEN r.status = 'aprobado' THEN 1 ELSE 0 END) AS ApprovedRequests,
        SUM(CASE WHEN r.status = 'rechazado' THEN 1 ELSE 0 END) AS RejectedRequests,
        SUM(CASE WHEN r.status = 'pendiente' THEN 1 ELSE 0 END) AS PendingRequests,
        AVG(r.amount) AS AverageAmount,
        MAX(r.amount) AS MaxAmount,
        MIN(r.amount) AS MinAmount
    FROM 
        users u
        LEFT JOIN requests r ON u.id = r.user_id
    WHERE 
        (@UserId IS NULL OR u.id = @UserId)
    GROUP BY 
        u.id, u.email, u.full_name;
END
GO

-- 3. SP para obtener solicitudes pendientes de aprobación
CREATE OR ALTER PROCEDURE sp_GetPendingRequests
    @SupervisorId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        r.id AS RequestId,
        r.title AS RequestTitle,
        r.description AS RequestDescription,
        r.status AS RequestStatus,
        r.amount AS RequestAmount,
        r.expected_date AS ExpectedDate,
        r.created_at AS RequestCreatedAt,
        u.email AS RequestCreatorEmail,
        u.full_name AS RequestCreatorName,
        DATEDIFF(day, r.created_at, GETDATE()) AS DaysPending
    FROM 
        requests r
        INNER JOIN users u ON r.user_id = u.id
    WHERE 
        r.status = 'pendiente'
        AND (@SupervisorId IS NULL OR r.supervisor_id = @SupervisorId)
    ORDER BY 
        r.created_at ASC;
END
GO

-- 4. SP para obtener el historial completo de una solicitud
CREATE OR ALTER PROCEDURE sp_GetRequestHistory
    @RequestId INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Información básica de la solicitud
    SELECT 
        r.id AS RequestId,
        r.title AS RequestTitle,
        r.description AS RequestDescription,
        r.status AS CurrentStatus,
        r.amount AS RequestAmount,
        r.expected_date AS ExpectedDate,
        r.created_at AS RequestCreatedAt,
        r.updated_at AS RequestUpdatedAt,
        u.email AS RequestCreatorEmail,
        u.full_name AS RequestCreatorName,
        s.email AS SupervisorEmail,
        s.full_name AS SupervisorName
    FROM 
        requests r
        INNER JOIN users u ON r.user_id = u.id
        LEFT JOIN users s ON r.supervisor_id = s.id
    WHERE 
        r.id = @RequestId;

    -- Historial de cambios de estado
    SELECT 
        ar.id AS AuditId,
        ar.previous_status AS PreviousStatus,
        ar.new_status AS NewStatus,
        ar.comment AS Comment,
        ar.created_at AS ChangeDate,
        u.email AS ChangedByEmail,
        u.full_name AS ChangedByName
    FROM 
        audit_requests ar
        INNER JOIN users u ON ar.user_id = u.id
    WHERE 
        ar.request_id = @RequestId
        AND ar.action = 'status_change'
    ORDER BY 
        ar.created_at DESC;

    -- Comentarios
    SELECT 
        cr.id AS CommentId,
        cr.comment AS Comment,
        cr.created_at AS CommentDate,
        u.email AS CommentByEmail,
        u.full_name AS CommentByName
    FROM 
        comment_requests cr
        INNER JOIN users u ON cr.user_id = u.id
    WHERE 
        cr.request_id = @RequestId
    ORDER BY 
        cr.created_at DESC;
END
GO

-- 5. SP para obtener métricas generales del sistema
CREATE OR ALTER PROCEDURE sp_GetSystemMetrics
    @StartDate DATE = NULL,
    @EndDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Total de solicitudes
    SELECT 
        COUNT(*) AS TotalRequests,
        SUM(CASE WHEN status = 'aprobado' THEN 1 ELSE 0 END) AS ApprovedRequests,
        SUM(CASE WHEN status = 'rechazado' THEN 1 ELSE 0 END) AS RejectedRequests,
        SUM(CASE WHEN status = 'pendiente' THEN 1 ELSE 0 END) AS PendingRequests,
        AVG(amount) AS AverageAmount,
        SUM(amount) AS TotalAmount,
        AVG(DATEDIFF(day, created_at, GETDATE())) AS AverageProcessingTime
    FROM 
        requests
    WHERE 
        (@StartDate IS NULL OR created_at >= @StartDate)
        AND (@EndDate IS NULL OR created_at <= @EndDate);

    -- Solicitudes por mes
    SELECT 
        YEAR(created_at) AS Year,
        MONTH(created_at) AS Month,
        COUNT(*) AS RequestCount,
        SUM(amount) AS TotalAmount
    FROM 
        requests
    WHERE 
        (@StartDate IS NULL OR created_at >= @StartDate)
        AND (@EndDate IS NULL OR created_at <= @EndDate)
    GROUP BY 
        YEAR(created_at),
        MONTH(created_at)
    ORDER BY 
        YEAR(created_at) DESC,
        MONTH(created_at) DESC;

    -- Top 5 usuarios con más solicitudes
    SELECT TOP 5
        u.email AS UserEmail,
        u.full_name AS UserName,
        COUNT(r.id) AS RequestCount,
        SUM(r.amount) AS TotalAmount
    FROM 
        users u
        INNER JOIN requests r ON u.id = r.user_id
    WHERE 
        (@StartDate IS NULL OR r.created_at >= @StartDate)
        AND (@EndDate IS NULL OR r.created_at <= @EndDate)
    GROUP BY 
        u.id, u.email, u.full_name
    ORDER BY 
        COUNT(r.id) DESC;
END
GO 