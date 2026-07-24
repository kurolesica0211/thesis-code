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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Hugo de Bourbon de Parme (Carlos Hugo Roderik Sybren; born 20 January 1997), formerly Hugo Klynstra, is a member of the extended Dutch royal family as the son of Prince Carlos, Hereditary Duke of Parma.
He was the first great-grandchild of Queen Juliana of the Netherlands.
Born out of wedlock, he was denied titles and family rights by his father until the Dutch Council of State ruled in his favor in 2018, granting him the style and title of His Royal Highness Prince Carlos Hugo
Roderik Sybren de Bourbon de Parme.
Despite the ruling, he is neither a member of the Dutch royal house (although considered a member of the extended Dutch royal family) nor a member of the House of Bourbon-Parma and is not in the line of succession to the defunct Parmese throne.
Early life and family

Carlos Hugo Roderik Sybren Klynstra was born in Nijmegen on 20 January 1997 to Prince Carlos de Bourbon de Parme, Prince of Piacenza and his friend Brigitte Klynstra.
Due to being an illegitimate son, he was not born a prince.
His father told Dutch media that Hugo's birth was "his mother's wish" and an "independent decision", denying his son any family rights.
His maternal grandmother, Ingrid Pieksma-Klynstra, was the wife of Adolph Roderik Ernst Leopold, Count of Rechteren-Limpurg.
Through his father, he is a grandson of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands.
He is the first great-grandchild of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
He is also a great-grandson of Prince Xavier of Bourbon-Parma and Madeleine de Bourbon-Busset.
Upon the death of his grandfather, Carlos Hugo, in 2010, his father became the titular Duke of Parma and Piacenza, Carlist claimant to the Spanish throne, and the Head of the House of Bourbon-Parma.
According to a royal decree of Queen Beatrix in 1996, his father is also a Dutch prince.
He is the half-brother of Princess Luisa of Parma, Marchioness of Castell'Arquato, Princess Cecilia of Parma, Countess of Berceto and Prince Carlos of Parma, The Prince of Piacenza.
Legal dispute over title

Upon turning eighteen in 2015, Hugo went to court to have his surname changed from Klynstra to his father's surname, 'de Bourbon de Parme', and claimed the dutch noble title of prince.
The Hereditary Duke of Parma insisted that he had a formal agreement with Hugo's mother that their relationship was "no-strings-attached" and that there would be "no family entanglement" following Hugo's conception.
In 2016 the Ministry of Justice and Security ruled in favor of Hugo's claim and granted him the use of his father's surname.
On 28 February 2018, the Dutch Council of State ruled in Hugo's favor, stating that Dutch law on nobility was clear and that the circumstances of Hugo's birth are irrelevant, granting Hugo the right to claim both his father's surname and (dutch) noble title and address.
As such, he became His Royal Highness Prince Carlos Hugo Roderik Sybren de Bourbon de Parme.
The title of 'Prince(ss) de Bourbon de Parme' is a Dutch title, bestowed by Queen Beatrix in 1996, and does not mean that Hugo automatically became a member of the House of Bourbon-Parma.
The court ruling stated that membership to the House of Bourbon-Parma is "a private matter for the royal house itself".
As such, he is not in the line of succession to the defunct Parma throne.
Titles and styles

References




2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (d8bfbd8d-30d4-4a18-a8d2-d40143ff9917)
 Call ID: d8bfbd8d-30d4-4a18-a8d2-d40143ff9917
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (620eb47b-0d46-4b54-8f41-cb69cc440cb4)
 Call ID: 620eb47b-0d46-4b54-8f41-cb69cc440cb4
  Args:
    source: Margriet
    type: :Woman
  AssignClass (a84499ed-4da7-46c4-ab0d-4e3f7095322a)
 Call ID: a84499ed-4da7-46c4-ab0d-4e3f7095322a
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (0663ddf5-8a03-4836-963a-44e3e36350fe)
 Call ID: 0663ddf5-8a03-4836-963a-44e3e36350fe
  Args:
    source: Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    type: :Man
  AddLiteral (aa2a6ca9-6c70-4e1d-b958-8c327469c96b)
 Call ID: aa2a6ca9-6c70-4e1d-b958-8c327469c96b
  Args:
    literal_value: Hugo Klynstra
    relation: :formerlyKnownAs
    source: Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    literal_type: xsd:string
  AddLiteral (89651b00-3386-4e16-96c5-2d549bbffda3)
 Call ID: 89651b00-3386-4e16-96c5-2d549bbffda3
  Args:
    literal_type: xsd:date
    relation: :hasBirthYear
    source: Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    literal_value: 1997-01-20
  AssignClass (a6b0a50b-c533-446a-b82e-76d95cc3489f)
 Call ID: a6b0a50b-c533-446a-b82e-76d95cc3489f
  Args:
    source: Carlos_de_Bourbon_de_Parme
    type: :Man
  AssignClass (e1828e6c-d7c9-4539-9991-5b549b5f3c76)
 Call ID: e1828e6c-d7c9-4539-9991-5b549b5f3c76
  Args:
    source: Brigitte_Klynstra
    type: :Woman
  AddTriple (0ddc9415-d203-4411-8f21-ab9abd0d508f)
 Call ID: 0ddc9415-d203-4411-8f21-ab9abd0d508f
  Args:
    relation: :hasFather
    target: Carlos_de_Bourbon_de_Parme
    source: Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AddTriple (10988df3-f672-4644-994b-065bb0020404)
 Call ID: 10988df3-f672-4644-994b-065bb0020404
  Args:
    relation: :hasMother
    target: Brigitte_Klynstra
    source: Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AssignClass (c9f70a90-9da7-4b15-9e19-0e4af24145ca)
 Call ID: c9f70a90-9da7-4b15-9e19-0e4af24145ca
  Args:
    type: :Woman
    source: Juliana
  AssignClass (8c3b8f11-0726-44dc-aa68-0901a2b20494)
 Call ID: 8c3b8f11-0726-44dc-aa68-0901a2b20494
  Args:
    type: :Man
    source: Bernhard_of_Lippe_Biesterfeld
  AssignClass (d0258588-1606-4a79-baf0-db412ef7b2ed)
 Call ID: d0258588-1606-4a79-baf0-db412ef7b2ed
  Args:
    source: Carlos_Hugo_Duke_of_Parma
    type: :Man
  AssignClass (1dea4e51-c863-49f0-82f3-c97c61288905)
 Call ID: 1dea4e51-c863-49f0-82f3-c97c61288905
  Args:
    type: :Woman
    source: Irene_of_the_Netherlands
  AddTriple (8b4950a6-d292-45db-9443-1f016098e98b)
 Call ID: 8b4950a6-d292-45db-9443-1f016098e98b
  Args:
    target: Carlos_Hugo_Duke_of_Parma
    source: Carlos_de_Bourbon_de_Parme
    relation: :hasFather
  AddTriple (ff308e0d-e60c-4a49-95a9-0a77f5b70c28)
 Call ID: ff308e0d-e60c-4a49-95a9-0a77f5b70c28
  Args:
    relation: :hasMother
    source: Carlos_de_Bourbon_de_Parme
    target: Irene_of_the_Netherlands
  AssignClass (b9fbe6ca-1b69-47d8-8ec8-310650578605)
 Call ID: b9fbe6ca-1b69-47d8-8ec8-310650578605
  Args:
    source: Ingrid_Pieksma_Klynstra
    type: :Woman
  AssignClass (f3f48a36-9464-4b97-9595-6d4e8f4f1113)
 Call ID: f3f48a36-9464-4b97-9595-6d4e8f4f1113
  Args:
    type: :Man
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren_Limpurg
  AddTriple (034602f6-9ea0-405f-aa9c-ab6e3f22677a)
 Call ID: 034602f6-9ea0-405f-aa9c-ab6e3f22677a
  Args:
    relation: :hasMother
    source: Brigitte_Klynstra
    target: Ingrid_Pieksma_Klynstra
  AssignClass (af08d0c2-b12c-42cf-a251-786ac9575805)
 Call ID: af08d0c2-b12c-42cf-a251-786ac9575805
  Args:
    source: Xavier_of_Bourbon_Parma
    type: :Man
  AssignClass (0366274c-eb4c-4c80-9aee-87e858dd4528)
 Call ID: 0366274c-eb4c-4c80-9aee-87e858dd4528
  Args:
    source: Madeleine_de_Bourbon_Busset
    type: :Woman
  AssignClass (ac47cc77-5b95-46b8-8e6b-bc62dd4c2acb)
 Call ID: ac47cc77-5b95-46b8-8e6b-bc62dd4c2acb
  Args:
    source: Luisa_of_Parma
    type: :Woman
  AssignClass (e9bafae0-e24c-41cf-8eeb-2bdf3da60335)
 Call ID: e9bafae0-e24c-41cf-8eeb-2bdf3da60335
  Args:
    type: :Woman
    source: Cecilia_of_Parma
  AssignClass (395237dd-36b6-446e-b095-1609f744e227)
 Call ID: 395237dd-36b6-446e-b095-1609f744e227
  Args:
    type: :Man
    source: Carlos_of_Parma
  AddTriple (a612e3d7-e318-435c-8bf0-504162290dab)
 Call ID: a612e3d7-e318-435c-8bf0-504162290dab
  Args:
    relation: :hasFather
    target: Carlos_de_Bourbon_de_Parme
    source: Luisa_of_Parma
  AddTriple (190275a8-41ba-41d5-a51d-9fdefbc0b5c4)
 Call ID: 190275a8-41ba-41d5-a51d-9fdefbc0b5c4
  Args:
    target: Carlos_de_Bourbon_de_Parme
    source: Cecilia_of_Parma
    relation: :hasFather
  AddTriple (ae34fcce-fba1-44f1-ba75-f7faeb71e26d)
 Call ID: ae34fcce-fba1-44f1-ba75-f7faeb71e26d
  Args:
    relation: :hasFather
    source: Carlos_of_Parma
    target: Carlos_de_Bourbon_de_Parme
  Finish (509f5532-6713-4d03-981a-75514bdac744)
 Call ID: 509f5532-6713-4d03-981a-75514bdac744
  Args: