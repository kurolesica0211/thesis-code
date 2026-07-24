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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Margarita of Bourbon-Parma, Countess of Colorno (Dutch: Margarita Maria Beatrix Prinses de Bourbon de Parme; born 13 October 1972), is the eldest daughter of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Margarita de Bourbon de Parme in the Netherlands as a member of the extended royal family.
Early life

Born in Nijmegen, she is the twin sister of Prince Jaime.
She also has an elder brother, Prince Carlos, and a younger sister, Princess Carolina.
Her godparents are Queen Beatrix of the Netherlands (maternal aunt) and Prince Sixtus Henry of Bourbon-Parma (paternal uncle).
She is the eldest granddaughter of Queen Juliana and Prince Bernhard.
Together with her mother and her siblings she moved from Spain to The Netherlands, to live with her grandparents, Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld at Baarn.
Margarita studied Cultural Anthropology at the Vrije Universiteit of Amsterdam and is an interior decorator.
First marriage and controversy

On 19 June 2001, Princess Margarita married the entrepreneur Edwin Karel Willem de Roy van Zuydewijn, member of a Dutch patrician family.
In 2003, a series of incidents became known as the Margarita-affair.
Margarita and her husband accused the Dutch Royal House and the Dutch secret service of obstructing the affairs of Fincentives, the company of de Roy van Zuydewijn.
The couple's home was the Bartas Castle in Saint-Georges, Gers, France, but by 2004 the princess was increasingly seen more often in Amsterdam than there.
Because of the quarrels between the princess and the Dutch Royal family during the Margarita-affair, she was not welcome at the marriage of her cousin Willem-Alexander, Prince of Orange to Máxima Zorreguieta, or at the funeral of her uncle, Prince Claus of the Netherlands.
On 20 February 2023, Princess Margarita and Ten Cate announced their divorce.
Together they have two daughters:


Margarita currently lives in Wassenaar.
Titles, styles and honours

Already a ducal princess from birth, her father bestowed on 2 September 1996 the substantive title Contessa di Colorno (Countess of Colorno) upon her.
The same year she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest noble title Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana, she is officially a member of the more extended Dutch royal family.
Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (f7b3a3af-8b05-4a51-9d25-517f7866efb5)
 Call ID: f7b3a3af-8b05-4a51-9d25-517f7866efb5
  Args:
    type: :Woman
    source: Princess_Margarita_of_Bourbon-Parma
  AssignClass (4975e299-2d2f-41d9-9a46-a64b92d4eb02)
 Call ID: 4975e299-2d2f-41d9-9a46-a64b92d4eb02
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (6b4fc8a1-c1d2-4f9a-ba9f-6e89cc8697cc)
 Call ID: 6b4fc8a1-c1d2-4f9a-ba9f-6e89cc8697cc
  Args:
    source: Carlos_Hugo_Duke_of_Parma
    type: :Man
  AssignClass (20c52275-94d8-401e-9e18-ebc53e740a57)
 Call ID: 20c52275-94d8-401e-9e18-ebc53e740a57
  Args:
    source: Prince_Jaime
    type: :Man
  AssignClass (56467b8b-a134-4d90-a992-9ccbd10d46b8)
 Call ID: 56467b8b-a134-4d90-a992-9ccbd10d46b8
  Args:
    source: Prince_Carlos
    type: :Man
  AssignClass (85fb8cae-c314-4d30-885f-83e2b34bc157)
 Call ID: 85fb8cae-c314-4d30-885f-83e2b34bc157
  Args:
    source: Princess_Carolina
    type: :Woman
  AssignClass (ed9f869d-46c3-4964-8db2-a95f7e0f21d0)
 Call ID: ed9f869d-46c3-4964-8db2-a95f7e0f21d0
  Args:
    source: Queen_Juliana
    type: :Woman
  AssignClass (6f57e764-0cb3-435a-bb35-0eb273e5cfc0)
 Call ID: 6f57e764-0cb3-435a-bb35-0eb273e5cfc0
  Args:
    type: :Man
    source: Prince_Bernhard
  AssignClass (9640b6d7-31fd-4952-bdad-b5fcc16a27a5)
 Call ID: 9640b6d7-31fd-4952-bdad-b5fcc16a27a5
  Args:
    type: :Woman
    source: Queen_Beatrix
  AssignClass (89c248e0-00b2-45fc-9883-825c281762b9)
 Call ID: 89c248e0-00b2-45fc-9883-825c281762b9
  Args:
    type: :Man
    source: Prince_Sixtus_Henry_of_Bourbon-Parma
  AssignClass (d5a00d15-1690-4fb3-bfa5-dffcd12d4859)
 Call ID: d5a00d15-1690-4fb3-bfa5-dffcd12d4859
  Args:
    type: :Man
    source: Edwin_Karel_Willem_de_Roy_van_Zuydewijn
  AddTriple (057f230e-5285-4ed1-a215-98c2264b9ab1)
 Call ID: 057f230e-5285-4ed1-a215-98c2264b9ab1
  Args:
    relation: :hasMother
    source: Princess_Margarita_of_Bourbon-Parma
    target: Princess_Irene_of_the_Netherlands
  AddTriple (f89715bf-da26-4356-beb2-f0e17646aae3)
 Call ID: f89715bf-da26-4356-beb2-f0e17646aae3
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    target: Carlos_Hugo_Duke_of_Parma
    relation: :hasFather
  AddTriple (d19a4d6d-5406-43af-91e1-2d19bcd444cf)
 Call ID: d19a4d6d-5406-43af-91e1-2d19bcd444cf
  Args:
    relation: :isSisterOf
    target: Prince_Jaime
    source: Princess_Margarita_of_Bourbon-Parma
  AddTriple (a90ec5ca-9e2d-4c58-a8ed-ad8cd3641531)
 Call ID: a90ec5ca-9e2d-4c58-a8ed-ad8cd3641531
  Args:
    target: Princess_Margarita_of_Bourbon-Parma
    source: Prince_Carlos
    relation: :isBrotherOf
  AddTriple (97d0045a-f6e3-4eb2-8aab-183825ed3a2a)
 Call ID: 97d0045a-f6e3-4eb2-8aab-183825ed3a2a
  Args:
    target: Princess_Margarita_of_Bourbon-Parma
    source: Princess_Carolina
    relation: :isSisterOf
  AddLiteral (e26cad04-7e57-4678-a35b-e6334aa5bb56)
 Call ID: e26cad04-7e57-4678-a35b-e6334aa5bb56
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    literal_value: 1972
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (1b0bdb09-8e20-4a57-889b-54f5faada7fa)
 Call ID: 1b0bdb09-8e20-4a57-889b-54f5faada7fa
  Args:
    target: Queen_Juliana
    source: Princess_Irene_of_the_Netherlands
    relation: :hasMother
  AddTriple (c138838b-0c5b-4049-979b-6aab8e9ceaff)
 Call ID: c138838b-0c5b-4049-979b-6aab8e9ceaff
  Args:
    relation: :hasFather
    source: Princess_Irene_of_the_Netherlands
    target: Prince_Bernhard
  AddLiteral (f62ce2b8-dba2-4ed1-aeef-970f048bcc7d)
 Call ID: f62ce2b8-dba2-4ed1-aeef-970f048bcc7d
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess_Margarita_of_Bourbon-Parma
    literal_value: 2001
  AddTriple (de8b5abf-07e0-44d2-a91d-fde7606bf34a)
 Call ID: de8b5abf-07e0-44d2-a91d-fde7606bf34a
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    target: Edwin_Karel_Willem_de_Roy_van_Zuydewijn
    relation: :hasRelation
  Finish (13148648-bb57-4b37-9afc-c5551d689068)
 Call ID: 13148648-bb57-4b37-9afc-c5551d689068
  Args: