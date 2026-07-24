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


Princess Claude of Orléans (Claude Marie Agnès Catherine; born 11 December 1943) is a French princess of the House of Orléans.
Biography

Family

Claude was born on 11 December 1943 in Larache, Morocco as the ninth child and fifth daughter of Henri, Count of Paris, Orléanist claimant to the French throne, and Princess Isabelle of Orléans-Braganza.
One of eleven siblings, Claude's eldest brother was Henri, Count of Paris, who succeeded their father as head of the Orléans family, and two of her sisters also became consorts of pretenders to abolished thrones; Anne, Duchess of Calabria and Diane, Duchess of Württemberg.
Marriage and issue

On 22 July 1964 in Sintra, Princess Claude married her second cousin, Prince Amedeo of Savoy, Duke of Aosta.
He was the only son of Prince Aimone, Duke of Aosta, second cousin once removed of Italy's last king, Umberto II.
Aimone was briefly made nominal head of an Italian puppet state during World War II as King Tomislav II of Croatia.
Claude was the third Orleanist princess to hold the title Duchess of Aosta by marriage.
The couple met while attending the wedding of Infante Juan Carlos of Spain and Princess Sophia of Greece and Denmark in May 1962 in Athens.
A Savoy family council having met at King Umberto's residence in exile at Cimiez, France, in the summer of 1963, another was held in London secretly at the king's hospital bedside to discuss the prospect of the king's only son Vittorio Emanuele, Prince of Naples, choosing to marry a commoner, Marina Doria, which had become the subject of much media speculation.
In view of his illness, Amedeo's imminent marriage to a suitable princess, and his son's ongoing relationship with Doria, Umberto contemplated publicly abdicating (having left Italy for exile in 1946 pursuant to an anti-monarchy plebiscite, he had not formally renounced) and recognizing Amedeo as the successor to his claim to Italy's abolished throne.
The wedding was attended by 300 guests, including King Umberto and the Prince and Princess of Spain.
After the duke completed his duties as a naval officer, the couple were given the Borro by Aimone's mother, a large estate in the Tuscan village of San Giustino Valdarno, near Fiesole, Italy, where they cultivated vineyards.
Amedeo was remarried later that year to Silvia Paternò di Spedalotto, while Claude remarried twice: civilly on 27 April 1982 in Port-au-Prince, Haiti with Luigi Arnaldo La Cagnina (divorced in 1996), a television journalist in the United States and Canada, and both civilly and religiously with Enrico Gandolfi in 2006 in Oreno, Milan.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (154e42d2-dfc0-430f-b01f-8393fcd552c3)
 Call ID: 154e42d2-dfc0-430f-b01f-8393fcd552c3
  Args:
    type: :Woman
    source: Princess_Claude_of_Orléans
  AssignClass (5d06c145-4044-4c80-b2e1-3e7abbb51e24)
 Call ID: 5d06c145-4044-4c80-b2e1-3e7abbb51e24
  Args:
    type: :Person
    source: Princess_Claude_of_Orléans
  AddLiteral (6b4ccfa4-3b21-44c3-b0db-eb2c26f01f57)
 Call ID: 6b4ccfa4-3b21-44c3-b0db-eb2c26f01f57
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess_Claude_of_Orléans
    literal_value: 1943
  AssignClass (a3fe161d-6186-4800-8d5e-4346fbee0388)
 Call ID: a3fe161d-6186-4800-8d5e-4346fbee0388
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (37179994-06fb-4d54-b0d5-986ceea303b1)
 Call ID: 37179994-06fb-4d54-b0d5-986ceea303b1
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AssignClass (54e48d30-a5da-40f0-8ec4-6757319a5f7e)
 Call ID: 54e48d30-a5da-40f0-8ec4-6757319a5f7e
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orléans-Braganza
  AssignClass (466b3283-a84e-4659-a323-1484d3a39b21)
 Call ID: 466b3283-a84e-4659-a323-1484d3a39b21
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orléans-Braganza
  AddTriple (198e3fb8-6181-444a-9055-30b08f8cf2e1)
 Call ID: 198e3fb8-6181-444a-9055-30b08f8cf2e1
  Args:
    relation: :hasFather
    source: Princess_Claude_of_Orléans
    target: Henri_Count_of_Paris
  AddTriple (7ff5a85b-007c-4a83-997a-bb03f30bae44)
 Call ID: 7ff5a85b-007c-4a83-997a-bb03f30bae44
  Args:
    relation: :hasMother
    source: Princess_Claude_of_Orléans
    target: Princess_Isabelle_of_Orléans-Braganza
  AssignClass (c12fe00f-5a63-405e-973e-7da63daccff6)
 Call ID: c12fe00f-5a63-405e-973e-7da63daccff6
  Args:
    type: :Man
    source: Henri_Count_of_Paris_jr
  AssignClass (7d99f147-002c-4305-8740-0cf2099b2193)
 Call ID: 7d99f147-002c-4305-8740-0cf2099b2193
  Args:
    type: :Person
    source: Henri_Count_of_Paris_jr
  AddTriple (5d6bceb2-2786-4efa-a8fd-6ccecff8b454)
 Call ID: 5d6bceb2-2786-4efa-a8fd-6ccecff8b454
  Args:
    target: Henri_Count_of_Paris_jr
    source: Princess_Claude_of_Orléans
    relation: :hasBrother
  AssignClass (8d8deb73-0948-4220-8a09-a5826272f215)
 Call ID: 8d8deb73-0948-4220-8a09-a5826272f215
  Args:
    type: :Woman
    source: Anne_Duchess_of_Calabria
  AssignClass (df92876f-f56a-4136-b00c-3e72858d243f)
 Call ID: df92876f-f56a-4136-b00c-3e72858d243f
  Args:
    type: :Person
    source: Anne_Duchess_of_Calabria
  AddTriple (bc9d7a01-d3da-4e10-af53-e184f7eb4a59)
 Call ID: bc9d7a01-d3da-4e10-af53-e184f7eb4a59
  Args:
    target: Anne_Duchess_of_Calabria
    relation: :hasSister
    source: Princess_Claude_of_Orléans
  AssignClass (a2c5c316-945e-401e-8c4a-d69315b6c807)
 Call ID: a2c5c316-945e-401e-8c4a-d69315b6c807
  Args:
    type: :Woman
    source: Diane_Duchess_of_Württemberg
  AssignClass (8847612a-5092-4401-b9a8-48765c943fa9)
 Call ID: 8847612a-5092-4401-b9a8-48765c943fa9
  Args:
    type: :Person
    source: Diane_Duchess_of_Württemberg
  AddTriple (161ed012-18f2-4bf6-8452-4e0a48741565)
 Call ID: 161ed012-18f2-4bf6-8452-4e0a48741565
  Args:
    target: Diane_Duchess_of_Württemberg
    relation: :hasSister
    source: Princess_Claude_of_Orléans
  AssignClass (c0bb1e1b-b28d-4daf-a122-1b2228b8caf3)
 Call ID: c0bb1e1b-b28d-4daf-a122-1b2228b8caf3
  Args:
    type: :Man
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
  AssignClass (d00fcd5e-886b-4c5c-afea-f5fd5480cd22)
 Call ID: d00fcd5e-886b-4c5c-afea-f5fd5480cd22
  Args:
    type: :Person
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
  AddLiteral (88eebf12-169b-402f-86c5-3f390c1fc6d0)
 Call ID: 88eebf12-169b-402f-86c5-3f390c1fc6d0
  Args:
    literal_type: xsd:integer
    source: Princess_Claude_of_Orléans
    relation: :hasMarriageYear
    literal_value: 1964
  AddTriple (854b18aa-459a-4488-9276-ae0e3d8941ff)
 Call ID: 854b18aa-459a-4488-9276-ae0e3d8941ff
  Args:
    target: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    relation: :hasRelation
    source: Princess_Claude_of_Orléans
  AssignClass (84747c4f-5b1c-4502-8a24-de42a9702b2b)
 Call ID: 84747c4f-5b1c-4502-8a24-de42a9702b2b
  Args:
    type: :Man
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (2a108845-ac47-4205-9fb4-b7a44eee3211)
 Call ID: 2a108845-ac47-4205-9fb4-b7a44eee3211
  Args:
    type: :Person
    source: Prince_Aimone_Duke_of_Aosta
  AddTriple (a55d03f7-3d7c-493f-bef8-a9846a4d4b9a)
 Call ID: a55d03f7-3d7c-493f-bef8-a9846a4d4b9a
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
  AssignClass (f14d183b-1029-4512-9d5d-db4b344ed94b)
 Call ID: f14d183b-1029-4512-9d5d-db4b344ed94b
  Args:
    type: :Man
    source: Luigi_Arnaldo_La_Cagnina
  AssignClass (f385f447-4247-4834-9548-753d8fcf8f15)
 Call ID: f385f447-4247-4834-9548-753d8fcf8f15
  Args:
    type: :Person
    source: Luigi_Arnaldo_La_Cagnina
  AddLiteral (846bafee-93de-4590-a82a-0159e3baa7a3)
 Call ID: 846bafee-93de-4590-a82a-0159e3baa7a3
  Args:
    literal_value: 1982
    relation: :hasMarriageYear
    source: Princess_Claude_of_Orléans
    literal_type: xsd:integer
  AddTriple (9cfe5ec2-80ae-412e-abc4-381e3d15fbf3)
 Call ID: 9cfe5ec2-80ae-412e-abc4-381e3d15fbf3
  Args:
    target: Luigi_Arnaldo_La_Cagnina
    source: Princess_Claude_of_Orléans
    relation: :hasRelation
  AssignClass (2ec68532-9cde-4025-937d-4f82b8feeeff)
 Call ID: 2ec68532-9cde-4025-937d-4f82b8feeeff
  Args:
    type: :Man
    source: Enrico_Gandolfi
  AssignClass (8efbae4f-299c-4832-99a8-77be9a37a850)
 Call ID: 8efbae4f-299c-4832-99a8-77be9a37a850
  Args:
    type: :Person
    source: Enrico_Gandolfi
  AddLiteral (2189a12b-c71d-4028-b93e-354cb508fc56)
 Call ID: 2189a12b-c71d-4028-b93e-354cb508fc56
  Args:
    literal_value: 2006
    source: Princess_Claude_of_Orléans
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (b9a1a181-60ce-423b-9e6a-4016d47c9f61)
 Call ID: b9a1a181-60ce-423b-9e6a-4016d47c9f61
  Args:
    source: Princess_Claude_of_Orléans
    relation: :hasRelation
    target: Enrico_Gandolfi
  AssignClass (8ec2c3d1-b340-4456-b5b0-27cd81bd27da)
 Call ID: 8ec2c3d1-b340-4456-b5b0-27cd81bd27da
  Args:
    type: :Woman
    source: Silvia_Paternò_di_Spedalotto
  AssignClass (616b7b56-34ee-4d39-8037-d61100dd84a5)
 Call ID: 616b7b56-34ee-4d39-8037-d61100dd84a5
  Args:
    type: :Person
    source: Silvia_Paternò_di_Spedalotto
  AddTriple (3a2bad77-d8dc-459d-84f1-18ec98e41da1)
 Call ID: 3a2bad77-d8dc-459d-84f1-18ec98e41da1
  Args:
    relation: :hasRelation
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    target: Silvia_Paternò_di_Spedalotto
  Finish (17e3eee7-465f-4b84-b2f8-5b1dd17e6045)
 Call ID: 17e3eee7-465f-4b84-b2f8-5b1dd17e6045
  Args: