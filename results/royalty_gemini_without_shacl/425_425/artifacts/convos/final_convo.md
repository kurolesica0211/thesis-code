================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
The Prince


Princess Marie Christine





Princess Josephine


The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Princess Marie of Liechtenstein (née Princess Marie Isabelle Marguerite Anne Geneviève of Orléans; born Boulogne-Billancourt, France on 3 January 1959) is the eldest daughter of Prince Henri, Count of Paris, Duke of France and his former wife Duchess Marie Thérèse of Württemberg.
She is the wife of Prince Gundakar of Liechtenstein, a great-grandson of Prince Alfred of Liechtenstein.
Youth

Her paternal grandfather, the Comte de Paris, head of the Orléanist House of France, received a letter of congratulations upon the princess's birth from General Charles de Gaulle.
Baptised 17 days after her birth by Maurice, Cardinal Feltin, the Archbishop of Paris, in the chapel of the Archdiocese, her god-parents were two of her grandparents; Philipp Albrecht, Duke of Wurttemberg and Isabelle d'Orléans, Duchess of Guise.


Princess Marie's early childhood was spent in Paris where, from October 1959 to April 1962, her father worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
For some months in that year Marie attended a private, parochial day school in Paris, before being sent to boarding school at Cours Dupanloup in Boulogne-sur-Seine in 1968 and Sacré-Coeur de Saint-Maur.
Upon receiving her bac, Marie enrolled at the Institut Catholique de Paris where she obtained a language interpretation degree in German and English after completing the Institut Supérieur d'Interprétariat et de Traduction curriculum.
Career

As the eldest of five children, two of whom are intellectually disabled, much of Princess Marie's professional and volunteer work has been in behalf of children with special needs.
In 1984 Marie moved back to Geneva to organise the Enfants et Jeunes de la rue ("Street Kids") programme as part of the BICE, conducting outreach in various countries, including Colombia and Brazil.
Transferred by BICE back to Paris, the princess became head of the Commission on Special Medical-Pedagogical Services, which sponsors humanitarian conferences in Europe and the developing world.
Marriage

While on work assignment in Rio de Janeiro in September 1988, Marie attended a dinner hosted by Princess Isabel of Brazil (born 1944), where she met their mutual cousin Prince Gundakar of Liechtenstein (grandson of Prince Alfred Roman of Liechtenstein).
Marie and Gundakar encountered each other again in November 1988 at the wedding of two more mutual cousins, Duchess Mathilde of Wurttemberg and the Hereditary Count Erich von Waldburg-Zeil.
On 11 February 1989 the couple were received by Marie's paternal grandfather, Monseigneur the Count of Paris, at his Chantilly estate, after which the couple's betrothal was announced to the media (the fiancée's father had been informed of the engagement earlier that day by a hand-delivered letter written by Marie's mother, Marie Thérèse of Württemberg, Duchess of Montpensier.
Although the Count of Clermont stated in a 12 May 1989 Point de Vue interview that it had been three years since he had seen Marie, he and his second wife, Michaela Cousino, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Clermont further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
However, it was on this occasion that Clermont learned that he would not be escorting Marie to her bridesgroom during the wedding.
Meanwhile, the Duchess of Montpensier had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of the Count of Paris, the head of the dynasty who, until then, had largely sided with the Duchess de Montpensier in opposition to the dissolution of his son's first marriage.
Moreover, the duchess had also rebuffed Monseigneur's offers to host the wedding at the Chapelle royale de Dreux or to commission the wedding gown from a major French haute couturier.
Her grandfather reportedly called the decision "treason", as tradition dictated that a French princess of the Blood Royal weds in France unless the groom is the ruler or heir apparent of a foreign realm.
Princess Marie spent much time there in her youth during visits to her maternal grandparents.
However, because her mother's brother Carl, Duke of Wurttemberg, now lived there with his wife Diane d'Orléans, sister of the Count of Clermont and daughter of the Count of Paris, relatives and members of foreign royal dynasties found themselves being urged by two sets of siblings, long married to each other, to take opposite sides in the families' quarrel.
Marie declared, "It's in that castle that I've been happiest.
Marie wed her prince civilly at Dreux's city hall on 22 July 1989, and religiously in the castle church of Friedrichshafen, on 29 July 1989.
Only eight persons, including bride and groom, attended the civil wedding in France (including the Duchess of Montpensier, her son Prince Jean, Duke of Vendôme, and a brother of the groom).
Although 250 guests attended the ceremony in Germany, absent were the Count of Clermont, the Count of Paris and all but two of Clermont's eight siblings; the hostess Diane, Duchess of Wurttemberg, was present, as was her brother Prince Jacques, Duke of Orléans, and their mother, Madame the Countess of Paris.
This was the first marriage of a member of the House of Orléans into a reigning dynasty since the 1929 wedding of Princess Françoise of Orléans to Prince Christopher of Greece.
Gundakar is a third cousin of his sovereign, Hans Adam II of Liechtenstein, and is in the line of succession to that principality's throne.
Gundakar Albert Alfred Petrus of Liechtenstein is the eldest son of Prince Johann of Liechtenstein and Princess Clothilde of Thurn und Taxis.
He has a twin sister, Princess Diemut, and five younger siblings.
Children

The couple have five children together:


Princess Marie Isabelle is the godmother of Infanta Maria Francisca of Portugal and Princess Thérèse d'Orléans.


Honours

Titles:



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (605cb0fb-a51c-4c15-9169-0f7d5cd80f9b)
 Call ID: 605cb0fb-a51c-4c15-9169-0f7d5cd80f9b
  Args:
    type: :Woman
    source: Princess Marie of Liechtenstein
  AssignClass (eeab456f-edca-4b9c-b4c0-7d16725b2098)
 Call ID: eeab456f-edca-4b9c-b4c0-7d16725b2098
  Args:
    source: Prince Henri, Count of Paris
    type: :Man
  AssignClass (fcf93b92-486c-4337-bc4a-f764cdb43db8)
 Call ID: fcf93b92-486c-4337-bc4a-f764cdb43db8
  Args:
    type: :Woman
    source: Duchess Marie Thérèse of Württemberg
  AddTriple (d73134ca-7ed0-4670-adee-7a5239a6f4cf)
 Call ID: d73134ca-7ed0-4670-adee-7a5239a6f4cf
  Args:
    target: Prince Henri, Count of Paris
    source: Princess Marie of Liechtenstein
    relation: :hasFather
  AddTriple (a2a5b87c-7ecd-48a1-bb2c-5cf57f9c7abd)
 Call ID: a2a5b87c-7ecd-48a1-bb2c-5cf57f9c7abd
  Args:
    target: Duchess Marie Thérèse of Württemberg
    relation: :hasMother
    source: Princess Marie of Liechtenstein
  AssignClass (fcfb077e-9475-425a-aa8a-8f6642a1bdd6)
 Call ID: fcfb077e-9475-425a-aa8a-8f6642a1bdd6
  Args:
    type: :Man
    source: Prince Gundakar of Liechtenstein
  AddTriple (5c975998-5784-413e-a1bd-f55758895c54)
 Call ID: 5c975998-5784-413e-a1bd-f55758895c54
  Args:
    source: Princess Marie of Liechtenstein
    relation: :hasRelation
    target: Prince Gundakar of Liechtenstein
  AddLiteral (112a7268-26ab-42c6-935d-bd12958155b2)
 Call ID: 112a7268-26ab-42c6-935d-bd12958155b2
  Args:
    literal_value: 1989
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess Marie of Liechtenstein
  AssignClass (72011e8b-4e85-49a9-bb36-9dccbcf64171)
 Call ID: 72011e8b-4e85-49a9-bb36-9dccbcf64171
  Args:
    source: Prince Johann of Liechtenstein
    type: :Man
  AssignClass (fb64abac-2dbf-41b2-b385-54df7249ee39)
 Call ID: fb64abac-2dbf-41b2-b385-54df7249ee39
  Args:
    type: :Woman
    source: Princess Clothilde of Thurn und Taxis
  AddTriple (4376c5c1-d02a-446d-bc63-d9df6bbc545d)
 Call ID: 4376c5c1-d02a-446d-bc63-d9df6bbc545d
  Args:
    source: Prince Gundakar of Liechtenstein
    relation: :hasFather
    target: Prince Johann of Liechtenstein
  AddTriple (b2eb3157-0e7f-4be9-a8d5-bdae449d1a10)
 Call ID: b2eb3157-0e7f-4be9-a8d5-bdae449d1a10
  Args:
    target: Princess Clothilde of Thurn und Taxis
    source: Prince Gundakar of Liechtenstein
    relation: :hasMother
  AssignClass (3d050bf3-334d-4d87-8b06-ef9045767f3d)
 Call ID: 3d050bf3-334d-4d87-8b06-ef9045767f3d
  Args:
    source: Princess Diemut
    type: :Woman
  AddTriple (ea6dbd1f-7ad4-4804-b2ef-425feace7876)
 Call ID: ea6dbd1f-7ad4-4804-b2ef-425feace7876
  Args:
    target: Prince Gundakar of Liechtenstein
    relation: :isSisterOf
    source: Princess Diemut
  AddTriple (1ab3de89-b9e9-43d1-afec-4cd7a0367d6e)
 Call ID: 1ab3de89-b9e9-43d1-afec-4cd7a0367d6e
  Args:
    relation: :hasFather
    source: Princess Diemut
    target: Prince Johann of Liechtenstein
  AddTriple (710f0382-bf28-4f32-a8d1-cf4c587c46c2)
 Call ID: 710f0382-bf28-4f32-a8d1-cf4c587c46c2
  Args:
    relation: :hasMother
    source: Princess Diemut
    target: Princess Clothilde of Thurn und Taxis
  AssignClass (bca353fd-0028-457c-92cd-5f70b1bad685)
 Call ID: bca353fd-0028-457c-92cd-5f70b1bad685
  Args:
    source: Philipp Albrecht, Duke of Wurttemberg
    type: :Man
  AssignClass (a8deb0da-1d91-4dd6-a3f9-364971c14c21)
 Call ID: a8deb0da-1d91-4dd6-a3f9-364971c14c21
  Args:
    source: Isabelle d'Orléans, Duchess of Guise
    type: :Woman
  Finish (585fe214-3e83-452a-adf2-af12a3eb7f3b)
 Call ID: 585fe214-3e83-452a-adf2-af12a3eb7f3b
  Args: