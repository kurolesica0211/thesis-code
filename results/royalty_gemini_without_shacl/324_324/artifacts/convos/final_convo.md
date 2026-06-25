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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (fce65458-921d-41fb-b123-ae59b2d15fa4)
 Call ID: fce65458-921d-41fb-b123-ae59b2d15fa4
  Args:
    type: :Man
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (9833b5b3-55ad-499f-b29f-d0b5dd4b7cd9)
 Call ID: 9833b5b3-55ad-499f-b29f-d0b5dd4b7cd9
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    type: :Person
  AddLiteral (57637065-3cf0-464e-88c6-e0f43a4325a9)
 Call ID: 57637065-3cf0-464e-88c6-e0f43a4325a9
  Args:
    literal_type: xsd:integer
    literal_value: 1933
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBirthYear
  AddLiteral (d78d2605-0641-4200-84ae-967bbcea47bf)
 Call ID: d78d2605-0641-4200-84ae-967bbcea47bf
  Args:
    literal_value: 2019
    literal_type: xsd:integer
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasDeathYear
  AssignClass (96c7810f-5bdc-43a6-b211-be4643a5effa)
 Call ID: 96c7810f-5bdc-43a6-b211-be4643a5effa
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (1f6681ed-975f-431a-8a92-eca4b471aa47)
 Call ID: 1f6681ed-975f-431a-8a92-eca4b471aa47
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddLiteral (eb120171-2f2c-4945-a12f-0c2b711ac255)
 Call ID: eb120171-2f2c-4945-a12f-0c2b711ac255
  Args:
    literal_value: 1908
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Henri_Count_of_Paris
  AddLiteral (9bebe967-56e3-481d-b4d1-2c84626f1080)
 Call ID: 9bebe967-56e3-481d-b4d1-2c84626f1080
  Args:
    relation: :hasDeathYear
    source: Henri_Count_of_Paris
    literal_value: 1999
    literal_type: xsd:integer
  AssignClass (7b3c30b4-ced4-46e7-a295-e236da1cb9dd)
 Call ID: 7b3c30b4-ced4-46e7-a295-e236da1cb9dd
  Args:
    source: Princess_Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (85fee414-e319-47fd-9b37-2b3dbe44c4ae)
 Call ID: 85fee414-e319-47fd-9b37-2b3dbe44c4ae
  Args:
    source: Princess_Isabelle_of_Orleans_Braganza
    type: :Person
  AddTriple (2f4f81a7-0527-44f9-9ae9-31ba07184634)
 Call ID: 2f4f81a7-0527-44f9-9ae9-31ba07184634
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Henri_Count_of_Paris
    relation: :hasFather
  AddTriple (fb0a593f-ba81-4479-9582-bd4ada7fe622)
 Call ID: fb0a593f-ba81-4479-9582-bd4ada7fe622
  Args:
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans_Braganza
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (e88a33cf-7698-479c-8b23-57b2b228505b)
 Call ID: e88a33cf-7698-479c-8b23-57b2b228505b
  Args:
    type: :Man
    source: Francois_brother_of_Henri
  AssignClass (ac5ffe4d-d61f-4da4-a10e-cb00a7bd74e8)
 Call ID: ac5ffe4d-d61f-4da4-a10e-cb00a7bd74e8
  Args:
    type: :Person
    source: Francois_brother_of_Henri
  AddTriple (36a0adeb-a775-4af2-bd22-a395c825a533)
 Call ID: 36a0adeb-a775-4af2-bd22-a395c825a533
  Args:
    relation: :isBrotherOf
    source: Francois_brother_of_Henri
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (097b30a0-bbd6-4c75-9bcf-da6ffea39b81)
 Call ID: 097b30a0-bbd6-4c75-9bcf-da6ffea39b81
  Args:
    type: :Woman
    source: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (441c803e-4467-4453-80c4-b0609ca18f56)
 Call ID: 441c803e-4467-4453-80c4-b0609ca18f56
  Args:
    source: Duchess_Marie_Therese_of_Wurttemberg
    type: :Person
  AddLiteral (ac3518a5-687d-4e06-8c44-3be1e3b26be6)
 Call ID: ac3518a5-687d-4e06-8c44-3be1e3b26be6
  Args:
    literal_type: xsd:integer
    literal_value: 1934
    source: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasBirthYear
  AddTriple (e7472332-dac9-44b0-bf13-690092853f10)
 Call ID: e7472332-dac9-44b0-bf13-690092853f10
  Args:
    relation: :hasRelation
    target: Duchess_Marie_Therese_of_Wurttemberg
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (104a871c-7582-49f9-835b-42858b18efba)
 Call ID: 104a871c-7582-49f9-835b-42858b18efba
  Args:
    relation: :hasMarriageYear
    source: Henri_Philippe_Pierre_Marie_dOrleans
    literal_type: xsd:integer
    literal_value: 1984
  AssignClass (d0f7ed5d-afe6-4873-a86c-1d536665d6ce)
 Call ID: d0f7ed5d-afe6-4873-a86c-1d536665d6ce
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Woman
  AssignClass (b21a4347-468f-4a59-a77b-01f696eace15)
 Call ID: b21a4347-468f-4a59-a77b-01f696eace15
  Args:
    type: :Person
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (be8adf31-8869-40ba-85ae-344eb951872f)
 Call ID: be8adf31-8869-40ba-85ae-344eb951872f
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasBirthYear
    literal_value: 1938
    literal_type: xsd:integer
  AddLiteral (05194fe1-202d-4273-be5c-872385eae1b4)
 Call ID: 05194fe1-202d-4273-be5c-872385eae1b4
  Args:
    relation: :hasDeathYear
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
    literal_value: 2022
  AddTriple (cf14bcc0-75e8-432f-8945-71b7d3525f03)
 Call ID: cf14bcc0-75e8-432f-8945-71b7d3525f03
  Args:
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
  AssignClass (d6a663d2-2cf4-44c0-af81-c818230a88a8)
 Call ID: d6a663d2-2cf4-44c0-af81-c818230a88a8
  Args:
    type: :Woman
    source: Marie_daughter_of_Henri
  AssignClass (5d512bce-a002-45fc-9d12-7217f2097a9d)
 Call ID: 5d512bce-a002-45fc-9d12-7217f2097a9d
  Args:
    source: Marie_daughter_of_Henri
    type: :Person
  AddTriple (a01e179a-c51f-4d1c-ad7d-ceee91357969)
 Call ID: a01e179a-c51f-4d1c-ad7d-ceee91357969
  Args:
    relation: :hasFather
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Marie_daughter_of_Henri
  AddTriple (8830c520-4b0e-43ed-93d4-d1ce568c446f)
 Call ID: 8830c520-4b0e-43ed-93d4-d1ce568c446f
  Args:
    source: Marie_daughter_of_Henri
    target: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasMother
  AssignClass (46e9a9a4-ba41-47dc-95e7-9e6d9dc1be1f)
 Call ID: 46e9a9a4-ba41-47dc-95e7-9e6d9dc1be1f
  Args:
    source: Prince_Gundakar_of_Liechtenstein
    type: :Man
  AssignClass (0812b6bb-6226-4131-bfd2-f53423a896eb)
 Call ID: 0812b6bb-6226-4131-bfd2-f53423a896eb
  Args:
    source: Prince_Gundakar_of_Liechtenstein
    type: :Person
  AddTriple (8ac11242-55a7-4831-8cb3-dd224fe3ed8d)
 Call ID: 8ac11242-55a7-4831-8cb3-dd224fe3ed8d
  Args:
    relation: :hasRelation
    target: Prince_Gundakar_of_Liechtenstein
    source: Marie_daughter_of_Henri
  AssignClass (a6e2c4c4-874b-468a-a726-6b00464b479e)
 Call ID: a6e2c4c4-874b-468a-a726-6b00464b479e
  Args:
    source: Michel_Count_of_Evreux
    type: :Man
  AssignClass (3b7aed80-2b6b-4151-a582-94265e7e1f38)
 Call ID: 3b7aed80-2b6b-4151-a582-94265e7e1f38
  Args:
    source: Michel_Count_of_Evreux
    type: :Person
  AddTriple (b1df7d32-f3b7-4d0f-81c5-b58396177f94)
 Call ID: b1df7d32-f3b7-4d0f-81c5-b58396177f94
  Args:
    source: Michel_Count_of_Evreux
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (60efe796-6012-423c-8116-b80fa6abfcb2)
 Call ID: 60efe796-6012-423c-8116-b80fa6abfcb2
  Args:
    type: :Man
    source: Thibaut_Count_of_La_Marche
  AssignClass (2f20e7cd-c9a4-4e63-862d-768172194b0b)
 Call ID: 2f20e7cd-c9a4-4e63-862d-768172194b0b
  Args:
    type: :Person
    source: Thibaut_Count_of_La_Marche
  AddTriple (53604879-ee08-4be8-95a3-2ca843ff8b55)
 Call ID: 53604879-ee08-4be8-95a3-2ca843ff8b55
  Args:
    source: Thibaut_Count_of_La_Marche
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (86badb4d-8bc4-44e0-b360-a8e59ea8903a)
 Call ID: 86badb4d-8bc4-44e0-b360-a8e59ea8903a
  Args:
    type: :Man
    source: Jacques_Duke_of_Orleans
  AssignClass (b947e0b8-c69a-4438-98ec-1ad86c7ed6db)
 Call ID: b947e0b8-c69a-4438-98ec-1ad86c7ed6db
  Args:
    source: Jacques_Duke_of_Orleans
    type: :Person
  AddTriple (c4d539b8-b259-464e-bf26-2042b139b411)
 Call ID: c4d539b8-b259-464e-bf26-2042b139b411
  Args:
    source: Jacques_Duke_of_Orleans
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (5a83284f-5d71-4082-93ba-f62114a5e017)
 Call ID: 5a83284f-5d71-4082-93ba-f62114a5e017
  Args:
    type: :Man
    source: Charles_Louis_dOrleans
  AssignClass (790cbead-a8fa-4601-9bd0-028b1ef5fa62)
 Call ID: 790cbead-a8fa-4601-9bd0-028b1ef5fa62
  Args:
    source: Charles_Louis_dOrleans
    type: :Person
  AddTriple (33d58578-58b4-4b49-ac6f-7ea2aec6592d)
 Call ID: 33d58578-58b4-4b49-ac6f-7ea2aec6592d
  Args:
    relation: :hasFather
    target: Jacques_Duke_of_Orleans
    source: Charles_Louis_dOrleans
  AssignClass (f761d5ac-c486-4749-9cd4-4b17151c4c41)
 Call ID: f761d5ac-c486-4749-9cd4-4b17151c4c41
  Args:
    type: :Man
    source: Foulques_dOrleans
  AssignClass (698c8f65-87c8-451d-9107-f1807a3f8566)
 Call ID: 698c8f65-87c8-451d-9107-f1807a3f8566
  Args:
    source: Foulques_dOrleans
    type: :Person
  AddTriple (582874d2-f90e-4731-9635-60be9b1be744)
 Call ID: 582874d2-f90e-4731-9635-60be9b1be744
  Args:
    source: Foulques_dOrleans
    target: Jacques_Duke_of_Orleans
    relation: :hasFather
  AssignClass (a3285312-19c4-4817-9199-aff1b8573fe4)
 Call ID: a3285312-19c4-4817-9199-aff1b8573fe4
  Args:
    source: Francois_son_of_Henri
    type: :Man
  AssignClass (e0c49e28-80bf-44c1-a5dd-2d812a8b27ed)
 Call ID: e0c49e28-80bf-44c1-a5dd-2d812a8b27ed
  Args:
    source: Francois_son_of_Henri
    type: :Person
  AddTriple (0bbe9dc4-7090-4f9f-bacc-dbf3c6b0fcd6)
 Call ID: 0bbe9dc4-7090-4f9f-bacc-dbf3c6b0fcd6
  Args:
    relation: :hasFather
    source: Francois_son_of_Henri
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (edad0064-9025-4343-831d-3b90fc43e02b)
 Call ID: edad0064-9025-4343-831d-3b90fc43e02b
  Args:
    source: Francois_son_of_Henri
    target: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasMother
  AssignClass (e4f096fa-8820-4e25-b3ea-3125bec0a602)
 Call ID: e4f096fa-8820-4e25-b3ea-3125bec0a602
  Args:
    type: :Man
    source: Jean_Duke_of_Vendome
  AssignClass (3c5f0216-8528-495b-b862-1de92e22f782)
 Call ID: 3c5f0216-8528-495b-b862-1de92e22f782
  Args:
    type: :Person
    source: Jean_Duke_of_Vendome
  AddTriple (f0ae8e17-04b3-4ae2-94b9-a3284cb43c74)
 Call ID: f0ae8e17-04b3-4ae2-94b9-a3284cb43c74
  Args:
    source: Jean_Duke_of_Vendome
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
  AddTriple (512b7955-7b0c-4fa4-833e-0f441de1aac9)
 Call ID: 512b7955-7b0c-4fa4-833e-0f441de1aac9
  Args:
    relation: :hasMother
    source: Jean_Duke_of_Vendome
    target: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (f6738786-d015-4515-bca6-29a56a1dcb89)
 Call ID: f6738786-d015-4515-bca6-29a56a1dcb89
  Args:
    source: Diane_sister_of_Henri
    type: :Woman
  AssignClass (3517ac67-91b1-4e7e-915f-6b67d905f0e3)
 Call ID: 3517ac67-91b1-4e7e-915f-6b67d905f0e3
  Args:
    source: Diane_sister_of_Henri
    type: :Person
  AddTriple (686bd135-3115-42b8-a3ed-547c66ae254a)
 Call ID: 686bd135-3115-42b8-a3ed-547c66ae254a
  Args:
    relation: :isSisterOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Diane_sister_of_Henri
  AssignClass (e7ee717f-5c4f-44cd-9d6f-39df4ee48dcc)
 Call ID: e7ee717f-5c4f-44cd-9d6f-39df4ee48dcc
  Args:
    source: Luis_Cousino_y_Sebire
    type: :Man
  AssignClass (af9dffc0-c43e-4b4d-a692-30402682ff3e)
 Call ID: af9dffc0-c43e-4b4d-a692-30402682ff3e
  Args:
    type: :Person
    source: Luis_Cousino_y_Sebire
  AssignClass (8955c783-53f5-4fb7-a605-8a2b63480018)
 Call ID: 8955c783-53f5-4fb7-a605-8a2b63480018
  Args:
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Woman
  AssignClass (19b7cd26-4323-474b-9258-ece05e23787d)
 Call ID: 19b7cd26-4323-474b-9258-ece05e23787d
  Args:
    type: :Person
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AddTriple (fbe45096-4e7c-43be-8a4c-3f8fc3233182)
 Call ID: fbe45096-4e7c-43be-8a4c-3f8fc3233182
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: Luis_Cousino_y_Sebire
    relation: :hasFather
  AddTriple (bce3843a-46a5-4226-b23e-a51dd4d5b388)
 Call ID: bce3843a-46a5-4226-b23e-a51dd4d5b388
  Args:
    relation: :hasMother
    target: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  Finish (c5cc5ecc-2b98-46ce-b3f3-440c966d5c6a)
 Call ID: c5cc5ecc-2b98-46ce-b3f3-440c966d5c6a
  Args: