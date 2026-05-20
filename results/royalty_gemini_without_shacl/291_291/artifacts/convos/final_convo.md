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
Princess Christina of the Netherlands (Maria Christina; 18 February 1947 – 16 August 2019) was the youngest of four daughters of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
She taught singing in New York and was a long-term supporter of the Youth Music Foundation in the Netherlands.
Christina died of bone cancer in 2019.
Early life

Princess Christina, who was known as Princess Marijke in her youth, was born on 18 February 1947, at Soestdijk Palace, Baarn, the Netherlands.
Her parents were Crown Princess Juliana, the only child of Queen Wilhelmina of the Netherlands, and Prince Bernhard of Lippe-Biesterfeld.
At the time of her birth, she was fifth in the line to the throne after her mother and three older sisters: Princess Beatrix, Princess Irene and Princess Margriet.
She was baptised on 9 October 1947 and her godparents included Queen Wilhelmina (her maternal grandmother), her eldest sister Princess Beatrix, Sir Winston Churchill (for whom her father stood proxy), her paternal grandmother Princess Armgard of Lippe-Biesterfeld, Prince Felix of Luxembourg, and his niece Princess Anne of Bourbon-Parma.
On 4 September 1948, after a reign of nearly 58 years, Christina's grandmother Queen Wilhelmina (68) abdicated the throne and her mother was inaugurated as Queen of the Kingdom of the Netherlands on 6 September 1948.
Childhood and education

While her mother was pregnant with Christina, she contracted either measles or rubella and as a result, Christina was born nearly blind.
In 1963, she stopped using her first name Maria, from then on referring to herself merely as Christina.
Marriage

While living in New York as Christina van Oranje, the Princess started a relationship with Cuban exile Jorge Guillermo.
Although societal attitudes were changing, because Guillermo was a Catholic, it was still possible that a marriage could cause a public scandal in the Netherlands such as the one that occurred in 1964 when Christina's sister Princess Irene married the Catholic Prince Carlos Hugo of Bourbon-Parma.
Accordingly, Princess Christina, at that time ninth in line for the Dutch throne, renounced her and her descendants' rights to the throne before officially announcing her engagement on St. Valentine's Day, 1975.
After their wedding, they lived in New York but later moved to the Netherlands, where they built Villa Eikenhorst  in Wassenaar, near The Hague.
She recorded and released several CDs (classical, Broadway) in 2000 and 2002, and was a long-term supporter of the Youth Music Foundation in the Netherlands.
In 1989, she allowed her name to be used for the Prinses Christina Concours, an annual competition held in the Netherlands to encourage the musical talents of children in the Netherlands.
One of her few public performances was at the marriage of her nephew Prince Bernhard Jr.
She also sang at the funerals of both of her parents Princess Juliana and Prince Bernhard in the New Church (Delft).
Early 2019, Christina made headlines when she decided to sell several works of art.
These works came to her through inheritance from the Dutch royal family: art lover William II of the Netherlands.
Death

In June 2018, it was announced that Princess Christina had been diagnosed with bone cancer.
Titles, styles and honours

Honours

National honours

Foreign honours

Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (db569ef2-52a2-4d12-9234-53e4fd0122e7)
 Call ID: db569ef2-52a2-4d12-9234-53e4fd0122e7
  Args:
    source: Princess_Christina_of_the_Netherlands
    type: :Woman
  AssignClass (17ca058e-18b0-4872-bbfe-084bd04b96a7)
 Call ID: 17ca058e-18b0-4872-bbfe-084bd04b96a7
  Args:
    type: :Person
    source: Princess_Christina_of_the_Netherlands
  AddLiteral (3a4c5857-b331-433d-aece-570bc6189e32)
 Call ID: 3a4c5857-b331-433d-aece-570bc6189e32
  Args:
    source: Princess_Christina_of_the_Netherlands
    literal_value: Female
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (023c4779-b9c0-4949-863f-ad6066bba30b)
 Call ID: 023c4779-b9c0-4949-863f-ad6066bba30b
  Args:
    source: Princess_Christina_of_the_Netherlands
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasBirthYear
  AddLiteral (b6cc2b59-b468-4f52-9528-f4abd9a0f604)
 Call ID: b6cc2b59-b468-4f52-9528-f4abd9a0f604
  Args:
    source: Princess_Christina_of_the_Netherlands
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2019
  AddLiteral (716a24e5-4581-44f5-a154-d3dc32db8e0f)
 Call ID: 716a24e5-4581-44f5-a154-d3dc32db8e0f
  Args:
    source: Princess_Christina_of_the_Netherlands
    literal_value: Princess Marijke
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AddLiteral (09a3d7b7-69d7-4391-9196-d9b409929216)
 Call ID: 09a3d7b7-69d7-4391-9196-d9b409929216
  Args:
    literal_type: xsd:string
    literal_value: Christina van Oranje
    relation: :alsoKnownAs
    source: Princess_Christina_of_the_Netherlands
  AssignClass (e4037359-3b4b-4183-a790-690a72eda100)
 Call ID: e4037359-3b4b-4183-a790-690a72eda100
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (33d0f5ea-258f-448a-a4fc-951d3649bce5)
 Call ID: 33d0f5ea-258f-448a-a4fc-951d3649bce5
  Args:
    source: Queen_Juliana_of_the_Netherlands
    type: :Ancestor
  AssignClass (e399198e-5904-4ce0-88cd-cf8a8c2ea7cb)
 Call ID: e399198e-5904-4ce0-88cd-cf8a8c2ea7cb
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (8dd4270b-b3dd-43e0-812d-8e94b5fafdd2)
 Call ID: 8dd4270b-b3dd-43e0-812d-8e94b5fafdd2
  Args:
    type: :Ancestor
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (f2860a4a-62ba-4665-9453-fb71174fb19a)
 Call ID: f2860a4a-62ba-4665-9453-fb71174fb19a
  Args:
    relation: :hasMother
    target: Queen_Juliana_of_the_Netherlands
    source: Princess_Christina_of_the_Netherlands
  AddTriple (7502d7f9-e3c9-4ca8-b90b-10cc273652d1)
 Call ID: 7502d7f9-e3c9-4ca8-b90b-10cc273652d1
  Args:
    source: Princess_Christina_of_the_Netherlands
    target: Prince_Bernhard_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (047eb920-1909-47d6-9445-2a6e4386b3cf)
 Call ID: 047eb920-1909-47d6-9445-2a6e4386b3cf
  Args:
    type: :Woman
    source: Queen_Wilhelmina_of_the_Netherlands
  AssignClass (f475feaa-b1df-423d-91f5-cdd549daa9a1)
 Call ID: f475feaa-b1df-423d-91f5-cdd549daa9a1
  Args:
    source: Queen_Wilhelmina_of_the_Netherlands
    type: :Ancestor
  AddTriple (431c71b8-8285-414b-afd0-6f4bf6efdb0f)
 Call ID: 431c71b8-8285-414b-afd0-6f4bf6efdb0f
  Args:
    target: Queen_Wilhelmina_of_the_Netherlands
    relation: :hasMother
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (18b92a6d-df34-46c6-a3ff-2024ecbfa10c)
 Call ID: 18b92a6d-df34-46c6-a3ff-2024ecbfa10c
  Args:
    source: Princess_Beatrix
    type: :Woman
  AssignClass (1685dbd4-de32-4ff4-ac82-4fb06a2e310d)
 Call ID: 1685dbd4-de32-4ff4-ac82-4fb06a2e310d
  Args:
    type: :Woman
    source: Princess_Irene
  AssignClass (756bec4e-dc77-466f-aa88-92e23b796e0c)
 Call ID: 756bec4e-dc77-466f-aa88-92e23b796e0c
  Args:
    source: Princess_Margriet
    type: :Woman
  AddTriple (56beb496-2eba-4948-9dce-f7cecf7b014d)
 Call ID: 56beb496-2eba-4948-9dce-f7cecf7b014d
  Args:
    relation: :isSisterOf
    target: Princess_Beatrix
    source: Princess_Christina_of_the_Netherlands
  AddTriple (8777df87-0b75-4854-bf05-ec04c8a58c66)
 Call ID: 8777df87-0b75-4854-bf05-ec04c8a58c66
  Args:
    target: Princess_Irene
    relation: :isSisterOf
    source: Princess_Christina_of_the_Netherlands
  AddTriple (156ba257-9558-4d85-8fbd-abc37a16b5e6)
 Call ID: 156ba257-9558-4d85-8fbd-abc37a16b5e6
  Args:
    target: Princess_Margriet
    relation: :isSisterOf
    source: Princess_Christina_of_the_Netherlands
  AssignClass (d41a3938-1e7c-4925-a3fe-0d5c04c20b78)
 Call ID: d41a3938-1e7c-4925-a3fe-0d5c04c20b78
  Args:
    source: Jorge_Guillermo
    type: :Man
  AssignClass (a653603f-938f-4f7f-950c-04d3089eaeef)
 Call ID: a653603f-938f-4f7f-950c-04d3089eaeef
  Args:
    type: :Person
    source: Jorge_Guillermo
  AddLiteral (3cd38f98-c600-47df-8e7e-4c9d4dba4bb4)
 Call ID: 3cd38f98-c600-47df-8e7e-4c9d4dba4bb4
  Args:
    source: Jorge_Guillermo
    literal_value: Male
    literal_type: xsd:string
    relation: :hasSex
  AddTriple (b840da09-8909-4074-b138-f3dd9bef5b1b)
 Call ID: b840da09-8909-4074-b138-f3dd9bef5b1b
  Args:
    target: Jorge_Guillermo
    relation: :hasRelation
    source: Princess_Christina_of_the_Netherlands
  AssignClass (ed73782f-454b-4dd2-85fb-b039a1a30861)
 Call ID: ed73782f-454b-4dd2-85fb-b039a1a30861
  Args:
    type: :Man
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
  AssignClass (734395a0-b3a5-4361-8c4b-91054591f7b1)
 Call ID: 734395a0-b3a5-4361-8c4b-91054591f7b1
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
    type: :Person
  AddTriple (3cf27d78-0491-4929-9f17-144253f5284b)
 Call ID: 3cf27d78-0491-4929-9f17-144253f5284b
  Args:
    source: Princess_Irene
    relation: :hasRelation
    target: Prince_Carlos_Hugo_of_Bourbon-Parma
  AssignClass (c00b6e42-1e67-4987-8fca-bc9b154ecafa)
 Call ID: c00b6e42-1e67-4987-8fca-bc9b154ecafa
  Args:
    source: Prince_Bernhard_Jr
    type: :Man
  AssignClass (0f0d4df7-153e-4cb9-8f84-675b8401995b)
 Call ID: 0f0d4df7-153e-4cb9-8f84-675b8401995b
  Args:
    source: Prince_Bernhard_Jr
    type: :Person
  AddTriple (47aab0d1-a43d-4e26-97cf-eb7234cff138)
 Call ID: 47aab0d1-a43d-4e26-97cf-eb7234cff138
  Args:
    target: Prince_Bernhard_Jr
    relation: :isBloodrelationOf
    source: Princess_Christina_of_the_Netherlands
  AssignClass (88d0e8fc-445b-4bb1-b813-deac031577bc)
 Call ID: 88d0e8fc-445b-4bb1-b813-deac031577bc
  Args:
    type: :Woman
    source: Princess_Armgard_of_Lippe-Biesterfeld
  AssignClass (15d92d02-8696-42ef-b6c4-386bd840e7ff)
 Call ID: 15d92d02-8696-42ef-b6c4-386bd840e7ff
  Args:
    source: Princess_Armgard_of_Lippe-Biesterfeld
    type: :Ancestor
  AssignClass (25c628c4-614d-4084-9c6d-f30624f85ca7)
 Call ID: 25c628c4-614d-4084-9c6d-f30624f85ca7
  Args:
    type: :Man
    source: Prince_Felix_of_Luxembourg
  AssignClass (60040a0a-8cbd-4656-80e4-8f3e808afde0)
 Call ID: 60040a0a-8cbd-4656-80e4-8f3e808afde0
  Args:
    source: Prince_Felix_of_Luxembourg
    type: :Ancestor
  AssignClass (d452a9ad-7ec2-4305-b272-5dd45bbd22ad)
 Call ID: d452a9ad-7ec2-4305-b272-5dd45bbd22ad
  Args:
    source: Princess_Anne_of_Bourbon-Parma
    type: :Woman
  AssignClass (c1aa51c5-78f4-4a8b-8b36-061860f73689)
 Call ID: c1aa51c5-78f4-4a8b-8b36-061860f73689
  Args:
    source: Princess_Anne_of_Bourbon-Parma
    type: :Person
  Finish (5efafa1a-8571-4851-8e8f-5f521c72979f)
 Call ID: 5efafa1a-8571-4851-8e8f-5f521c72979f
  Args: